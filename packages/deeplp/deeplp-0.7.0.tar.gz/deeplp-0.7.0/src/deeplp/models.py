import numpy as np
from tqdm import tqdm, tqdm_notebook
import torch
import torch.nn as nn
import torch.optim as optim

from colorama import just_fix_windows_console, init, Fore, Style
from typing import List, Callable, Optional, Tuple
from prettytable import PrettyTable, ALL

from deeplp.ode import createObjectiveFun, createPhi
from deeplp.utils import is_notebook


class PINN(nn.Module):
    def __init__(self, in_dim=2, out_dim=5, model_type="pinn"):
        super(PINN, self).__init__()
        # Input dimension becomes 2: one from t and one from the pooled b.
        self.fc1 = nn.Linear(in_dim, 100)
        self.activation1 = nn.Tanh()
        if model_type == "pinn":
            self.fc2 = nn.Linear(100, out_dim)
        else:
            self.fc2 = nn.Linear(100, 100)
            self.fc3 = nn.Linear(100, out_dim)
            self.activation2 = nn.ReLU()

        self.in_dim = in_dim
        self.out_dim = out_dim
        self.model_type = model_type

    def forward(self, tb):
        # If tb is a scalar, convert it to a 2D tensor with shape (1, in_dim)
        if tb.dim() == 0:
            tb = tb.unsqueeze(0).unsqueeze(1)
        elif tb.dim() == 1:
            tb = tb.unsqueeze(1)
        t = tb[:, 0].unsqueeze(1)  # Now safe because tb is at least 2D.
        x = self.activation1(self.fc1(tb))
        out = self.fc2(x)
        if self.model_type == "pinn":
            return (1 - torch.exp(-t)) * out
        else:
            out = self.activation2(out)
            out = self.fc3(out)
            return (1 - torch.exp(-t)) * out


# ------------------------------
# Define the vectorized loss function using functorch
# ------------------------------
def create_loss(
    model: PINN,
    tb: torch.Tensor,
    phi: Callable[[torch.Tensor], torch.Tensor],
):

    def loss_t():
        # ts: shape (N,) ; we need to work with scalar inputs, so we keep ts as a 1D tensor.
        # Evaluate the PINN on all collocation points.
        # The model expects input shape (N,1), so unsqueeze ts.
        ts_var = tb.clone().detach().requires_grad_(True)  # shape (N,)
        y_hat = model(ts_var.unsqueeze(1))

        def model_single(t):
            return model(t.unsqueeze(0)).squeeze(0)

        dy_dt = torch.vmap(torch.func.jacrev(model_single))(ts_var)  # shape: (N, 5)

        phi_y = torch.vmap(phi)(y_hat.squeeze(0))

        residuals = dy_dt - phi_y

        loss = torch.mean(torch.sum(residuals**2, dim=1))
        return loss

    def loss_b():
        """
        Compute the mean squared loss:
            loss = mean( || d/dt y_hat(tb) - phi(y_hat(tb), b) ||^2 )
        where tb is of shape (N, L) with L>=2:
        - tb[:, 0] contains time t (shape (N,1))
        - tb[:, 1:] contains b (shape (N, L-1))

        The function phi, when called as phi(b) with b of shape (L-1,), returns a function
        that accepts a single sample y (of shape (out_dim,)) and returns a tensor of shape (out_dim,).
        """
        # Ensure tb is differentiable.
        tb_var = tb.clone().detach().requires_grad_(True)  # shape: (N, L)

        # Evaluate model: y_hat will have shape (N, out_dim)
        y_hat = model(tb_var)
        # print("y_hat shape:", y_hat.shape)
        # print("y_hat:", y_hat)

        N = tb.shape[0]
        dy_dt = torch.zeros_like(y_hat)  # to store the derivative with respect to t

        # For each sample, compute the derivative of the model output with respect to t.
        for i in range(N):
            # Extract t: first column of tb_var for sample i.
            # t_val: shape (1, 1)
            t_val = tb_var[i, 0].unsqueeze(0).unsqueeze(1)
            # Extract b: remaining columns of tb_var for sample i.
            # b_val: shape (1, L-1)
            b_val = tb_var[i, 1:].unsqueeze(0)

            def single_sample(t_s):
                # t_s has shape (1,1). Concatenate with fixed b_val to form a full sample of shape (1, L)
                sample_input = torch.cat([t_s, b_val], dim=1)
                # Call the model and remove the batch dimension.
                return model(sample_input).squeeze(0)  # shape: (out_dim,)

            # Compute the directional derivative (Jacobian-vector product) with respect to t.
            # Here we compute d/dt at t_val in the direction of 1.
            _, jvp = torch.autograd.functional.jvp(
                single_sample, (t_val,), (torch.ones_like(t_val),)
            )
            dy_dt[i] = jvp  # shape (out_dim,)

        # Now, for each sample, apply the physics operator.
        phi_y_list = []
        for i in range(N):
            # For sample i, b_i is the parameter vector: shape (L-1,)
            b_i = tb_var[i, 1:]
            # Get the phi operator for this b.
            phi_func = phi(b_i)
            # Apply it to the model output for sample i.
            phi_y_list.append(phi_func(y_hat[i]))
        # Stack the results: shape (N, out_dim)
        phi_y = torch.stack(phi_y_list, dim=0)

        # Compute the residual and then the mean squared error.
        residuals = dy_dt - phi_y
        loss_val = torch.mean(torch.sum(residuals**2, dim=1))
        return loss_val

    if tb.shape[1] == 1:
        loss_fn = loss_t
    else:
        loss_fn = loss_b

    return loss_fn


# Save the model's state dictionary to a file


def create_batches(
    *,
    A: torch.Tensor | None = None,
    batch_size: int = 128,
    no_batches: int = 1,
    tspan: Tuple[float, float] = (0.0, 10.0),
    in_dim: int = 5,
    device: torch.device = torch.device("cpu"),
) -> List[Tuple[torch.Tensor, Optional[torch.Tensor]]]:
    # Create a list of time batches: each tensor has shape (batch_size, 1)
    ts_batches = [
        torch.empty(batch_size, dtype=torch.float32, device=device)
        .uniform_(*tspan)
        .unsqueeze(1)
        for _ in range(no_batches)
    ]
    if A is not None:
        assert isinstance(A, torch.Tensor) and A.dim() == 2, "A must be a 2D tensor"
        d_dim = A.shape[1]
        mean_A = torch.mean(A, dim=0)
        d_list = [
            mean_A
            * torch.empty(
                (batch_size, d_dim), dtype=torch.float32, device=device
            ).uniform_(*tspan)
            for _ in range(no_batches)
        ]
        return list(zip(ts_batches, d_list))
    else:
        if in_dim == 1:
            # Return a list of tuples (ts, None)
            return [(ts, None) for ts in ts_batches]
        else:
            # Create a list of b batches: each tensor has shape (batch_size, in_dim - 1)
            b_list = [
                torch.empty(
                    (batch_size, in_dim - 1), dtype=torch.float32, device=device
                ).uniform_(*tspan)
                for _ in range(no_batches)
            ]

            # Zip the two lists together into a list of tuples (ts, b)
            return list(zip(ts_batches, b_list))


def _load_model(filename, in_dim, out_dim, model_type: str):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = PINN(in_dim=in_dim, out_dim=out_dim, model_type=model_type)
    model.load_state_dict(torch.load(filename, map_location=device))
    model.eval()
    return model


def load_model(filename, in_dim, out_dim, *, model_type: str = "pinn"):
    model = _load_model(filename, in_dim, out_dim, model_type)

    def evaluate_it(T):
        t_tensor = torch.tensor(T, dtype=torch.float32, requires_grad=True)
        val = model(t_tensor)
        return val.detach().numpy().tolist()

    return evaluate_it


def train_model(
    A,
    b,
    D,
    name,
    tspan,
    case,
    epochs,
    batch_size,
    batches,
    device,
    *,
    model_type: str = "pinn",
):

    out_dim = sum(A.shape) if model_type == "pinn" else sum(A.shape) + sum(D.shape)

    def objecive_fun(b):
        if case in (1, 2):
            return createObjectiveFun(D)
        else:
            b_mean = torch.mean(b, dim=0)
            return createObjectiveFun(b_mean)

    if case == 1:
        phi = createPhi(D, A, model=model_type)
        in_dim = 1
        model, loss_list, mov_list = _train_model(
            phi(b),
            objecive_fun,
            tspan=tspan,
            in_dim=in_dim,
            out_dim=out_dim,
            batch_size=batch_size,
            no_batches=batches,
            epochs=epochs,
            lr=0.001,
            tol=1e-3,
            training_name=name,
            device=device,
            model_type=model_type,
        )
    elif case == 2:
        phi = createPhi(D, A, model=model_type)
        b_raw = b.tolist()
        in_dim = len(b_raw) + 1
        model, loss_list, mov_list = _train_model(
            phi,
            objecive_fun,
            tspan=tspan,
            in_dim=in_dim,
            out_dim=out_dim,
            batch_size=batch_size,
            no_batches=batches,
            epochs=epochs,
            lr=0.001,
            tol=1e-3,
            training_name=name,
            device=device,
            testing_tb=[tspan[1], *b_raw],
            model_type=model_type,
        )
    else:
        b_raw = D.tolist()
        in_dim = 1 + A.shape[1]
        phi = createPhi(None, A, b, model=model_type)
        model, loss_list, mov_list = _train_model(
            phi,
            objecive_fun,
            tspan=tspan,
            in_dim=in_dim,
            out_dim=out_dim,
            batch_size=batch_size,
            no_batches=batches,
            epochs=epochs,
            lr=0.001,
            tol=1e-3,
            training_name=name,
            device=device,
            testing_tb=[tspan[1], *b_raw],
            model_type=model_type,
        )

    return model, loss_list, mov_list


def _train_model(
    phi,  # physics operator generator: phi(b) returns a function to apply to model output.
    objective_fun,  # function that computes a scalar objective from model output.
    *,
    tspan: Tuple[float, float] = (0.0, 10.0),
    in_dim: int = 1,
    out_dim: int = 5,
    batch_size: int = 128,
    no_batches: int = 1,
    epochs: int = 1000,
    lr: float = 0.001,
    tol: float = 1e-5,
    training_name: str = "",
    device: torch.device = torch.device("cpu"),
    testing_tb: List[
        float
    ] = None,  # required when in_d im > 1; list of floats: first element is t, rest are b.
    model_type: str = "pinn",
):
    just_fix_windows_console()
    init()
    T = tspan[1]
    loss_list = []
    mov_list = []

    batched_data = create_batches(
        batch_size=batch_size,
        no_batches=no_batches,
        tspan=tspan,
        in_dim=in_dim,
        device=device,
    )
    if in_dim == 1:
        t_eval = torch.tensor(
            [[T]], dtype=torch.float32, device=device, requires_grad=True
        )
    else:
        # testing_tb should be provided as a list: first element is t, rest are b.
        t_eval = torch.tensor(
            [testing_tb], dtype=torch.float32, device=device, requires_grad=True
        )
    # Create the model using the provided in_dim.
    model = PINN(in_dim=in_dim, out_dim=out_dim, model_type=model_type).to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    print(Fore.RED + f"Starting training {training_name}" + Style.RESET_ALL)
    tqdm_fun = tqdm_notebook if is_notebook() else tqdm  #

    epoch_loss = 0.0

    # Use tqdm over ts_batches; we also need the index so we use enumerate.
    epoch_par = tqdm_fun(
        total=epochs,
        desc=f"Running {epochs} iterations".ljust(25),
        leave=False,
        ascii=True,
    )
    epoch = 1

    while True:
        loss_item = None
        val_item = None
        patch_par = tqdm_fun(
            batched_data,
            total=no_batches,
            desc=f"({no_batches} batches)".ljust(25),
            leave=False,
        )
        for ts, b in patch_par:
            tb = ts if b is None else torch.cat([ts, b], dim=1)
            compute_loss_vectorized = create_loss(model, tb, phi)
            optimizer.zero_grad()
            loss_val = compute_loss_vectorized()
            loss_val.backward()
            optimizer.step()
            loss_item = loss_val.item()
            y_pred = model(t_eval)
            val = objective_fun(b)(y_pred[0])
            val_item = val.item()
            patch_par.update(1)
            patch_par.set_postfix(loss=f"Patch: {loss_item:.6f}")

        # patch_par.reset()
        patch_par.clear()
        patch_par.close()

        loss_list.append(loss_item)
        mov_list.append(val_item)
        epoch_loss = loss_item
        if epoch == epochs:
            print(
                Fore.GREEN
                + f"{training_name} | Max iteration {epochs} reached: stopping training loss = {epoch_loss:.6f}"
                + Style.RESET_ALL
            )
            break
        epoch += 1
        epoch_par.update(1)
        epoch_par.set_postfix(loss=f"Epoch: {epoch_loss:.6f}")

        if epoch_loss < tol:
            print(
                Fore.GREEN
                + f"{training_name} | Stopping training at epoch {epoch} with loss = {epoch_loss:.6f}"
                + Style.RESET_ALL
            )
            break

    epoch_par.clear()
    epoch_par.close()

    # Evaluation step:

    print(Fore.BLUE + "Training complete.\n" + Style.RESET_ALL)
    return model, loss_list, mov_list


def test_model(model, dev, testing_list, case, T, objective):
    # ------------------------------
    # Evaluate the trained model at select time points
    # ------------------------------

    if case in [2, 3]:
        test_times = np.repeat(T, len(testing_list))
        _test_model(
            model,
            test_times,
            case=case,
            dev=dev,
            testing_points=testing_list,
            objective=objective,
        )
    else:
        test_times = [T]
        _test_model(
            model,
            test_times,
            dev=dev,
            objective=objective,
        )


def _test_model(
    model: PINN,
    test_times: List[float],
    *,
    case: int = 1,
    dev: torch.DeviceObjType = torch.device("cpu"),
    testing_points: List[List[float]] | None = None,
    objective: Callable[[torch.tensor], torch.tensor],
):
    assert (case != 1 and testing_points is not None) or (
        case == 1 and testing_points is None
    ), f"You must provide testing points for case {case}"
    table = PrettyTable()
    if case == 1:
        table.field_names = ["t", "ŷ(t)", "obj"]
    elif case == 2:
        table.field_names = ["t", "b", "ŷ(t)", "obj"]
        table.align["b"] = "l"
    else:
        table.field_names = ["t", "D", "ŷ(t)", "obj"]
        table.align["D"] = "l"

    table.align["t"] = "l"
    table.align["ŷ(t)"] = "l"
    # Set horizontal rules between every row
    table.hrules = ALL
    # Left-align each column

    for i, t in enumerate(test_times, start=1):
        if testing_points is not None:
            b = testing_points[i - 1]
            t_tensor = torch.tensor(
                [t, *b], dtype=torch.float32, device=dev, requires_grad=True
            ).unsqueeze(0)

            y_pred = model(t_tensor)

        else:
            t_tensor = torch.tensor(
                t, dtype=torch.float32, device=dev, requires_grad=True
            )
            y_pred = model(t_tensor)
        # Flatten the tensor and convert to a formatted string
        y_val = objective(y_pred)
        y_val_str = str(y_val.cpu().detach().numpy().flatten())
        y_pred_str = str(y_pred.cpu().detach().numpy().flatten())
        if case == 1:
            table.add_row([f"{t:6.2f}", y_pred_str, y_val_str])
        else:
            table.add_row(
                [f"{t:6.2f}", str(np.array(b).flatten()), y_pred_str, y_val_str]
            )

    # Print the entire table with color formatting
    print(Fore.MAGENTA + table.get_string() + Style.RESET_ALL)


# Get the current date in YYYY_MM_DD format
def save_model(model: PINN, name: str = "pinn_model"):

    # Create the filename with the date stamp
    filename = f"{name}_out_dim_{model.out_dim}.pt"

    # Save the model state dictionary
    torch.save(model.state_dict(), filename)

    print(f"saving... model in {filename}")


# def _train_model(
#     phi,  # physics operator generator: phi(b) returns a function to apply to model output.
#     objective_fun,  # function that computes a scalar objective from model output.
#     *,
#     tspan: Tuple[float, float] = (0.0, 10.0),
#     in_dim: int = 1,
#     out_dim: int = 5,
#     batch_size: int = 128,
#     no_batches: int = 1,
#     epochs: int = 1000,
#     lr: float = 0.001,
#     tol: float = 1e-5,
#     training_name: str = "",
#     device: torch.device = torch.device("cpu"),
#     testing_tb: List[
#         float
#     ] = None,  # required when in_d im > 1; list of floats: first element is t, rest are b.
#     model_type: str = "pinn",
# ):
#     just_fix_windows_console()
#     init()
#     T = tspan[1]
#     loss_list = []
#     mov_list = []

#     batched_data = create_batches(
#         batch_size=batch_size,
#         no_batches=no_batches,
#         tspan=tspan,
#         in_dim=in_dim,
#         device=device,
#     )
#     if in_dim == 1:
#         t_eval = torch.tensor(
#             [[T]], dtype=torch.float32, device=device, requires_grad=True
#         )
#     else:
#         # testing_tb should be provided as a list: first element is t, rest are b.
#         t_eval = torch.tensor(
#             [testing_tb], dtype=torch.float32, device=device, requires_grad=True
#         )
#     # Create the model using the provided in_dim.
#     model = PINN(in_dim=in_dim, out_dim=out_dim, model_type=model_type).to(device)
#     optimizer = optim.Adam(model.parameters(), lr=lr)
#     print(Fore.RED + f"Starting training {training_name}" + Style.RESET_ALL)
#     epoch = 1
#     tqdm_fun = tqdm_notebook if is_notebook() else tqdm  #
#     epoch_par = tqdm_fun(
#         total=epochs,
#         desc=f"Running {epochs} iterations".ljust(25),
#         leave=False,
#         ascii=True,
#     )

#     while True:
#         epoch_loss = 0.0
#         patch_par = tqdm_fun(
#             batched_data,
#             total=no_batches,
#             desc=f"({no_batches} batches)".ljust(25),
#             leave=False,
#         )
#         # Use tqdm over ts_batches; we also need the index so we use enumerate.
#         for ts, b in patch_par:
#             tb = ts if b is None else torch.cat([ts, b], dim=1)
#             compute_loss_vectorized = create_loss(model, tb, phi)
#             optimizer.zero_grad()
#             loss_val = compute_loss_vectorized()
#             loss_val.backward()
#             optimizer.step()
#             loss_item = loss_val.item()
#             epoch_loss += loss_item
#             loss_list.append(loss_item)
#             patch_par.set_postfix(loss=f"{loss_item:.6f}")
#             patch_par.update(1)
#             y_pred = model(t_eval)
#             val = objective_fun(b)(y_pred[0])
#             mov_list.append(val.item())
#         patch_par.clear()
#         epoch_loss /= no_batches

#         # if epoch % display_period == 0:
#         #     print(
#         #         Fore.MAGENTA
#         #         + f"{training_name} | {no_batches} batches, Epoch {epoch}/{epochs}: Loss = {epoch_loss:.6f}"
#         #         + Style.RESET_ALL
#         #     )
#         if epoch_loss < tol:
#             print(
#                 Fore.GREEN
#                 + f"{training_name} | Stopping training at epoch {epoch} with loss = {epoch_loss:.6f}"
#                 + Style.RESET_ALL
#             )
#             break
#         if epoch == epochs:
#             print(
#                 Fore.GREEN
#                 + f"{training_name} | Max iteration {epochs} reached: stopping training loss = {epoch_loss:.6f}"
#                 + Style.RESET_ALL
#             )
#             break

#         epoch += 1
#         epoch_par.set_postfix(loss=f"{loss_item:.6f}")
#         epoch_par.update(1)
#     epoch_par.close()
#     # Evaluation step:

#     print(Fore.BLUE + "Training complete.\n" + Style.RESET_ALL)
#     return model, loss_list, mov_list
