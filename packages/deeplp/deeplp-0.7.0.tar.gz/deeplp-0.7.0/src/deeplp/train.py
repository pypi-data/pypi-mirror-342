from collections import namedtuple
from typing import Callable, List
import torch
import numpy as np

import os

from deeplp.ode import createObjectiveFun
from deeplp.problems import Problem, pretty_print_lp, get_all_problems
from deeplp.models import (
    train_model,
    save_model,
    test_model,
)


# Import the module using importlib (the file must be in your Python path)

# Use inspect.getmembers to retrieve all functions defined in the module.
# This returns a list of tuples (name, function).


# os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import matplotlib.pyplot as plt

from deeplp.utils import get_file_name


Solution = namedtuple("Solution", ["solution", "model", "loss_list", "mov_lis"])


def plot_data(filename, title, ylabel):
    # Assume loss_list is a list of float loss values collected during training
    # Load loss_list from the text file.
    data_array = np.loadtxt(filename)
    # Convert to a Python list if needed:
    data_list = data_array.tolist()
    plt.figure(figsize=(8, 5))
    plt.plot(data_list, label=title)
    plt.xlabel("Iteration")
    plt.ylabel(ylabel)
    plt.title(f"{title} Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


def save_lists_to_file(loss_list, mov_list, filename):
    np_loss = np.array(loss_list)
    loss_filename = f"{filename}_loss.txt"
    print(f"saving... loss list in {loss_filename}")
    np.savetxt(loss_filename, np_loss, fmt="%.6f")

    movs_filename = f"{filename}_mov.txt"
    np_movs = np.array(mov_list)
    print(f"saving... movs list in {movs_filename}")
    np.savetxt(movs_filename, np_movs, fmt="%.6f")


# Example 1: Solving one LP with 4 variables and 1 constraint


def _train(
    batches: int,
    batch_size: int,
    epochs: int,
    problem: Problem,
    cases: List[int],
    do_plot: bool,
    saving_dir: str | None,
    device: torch.device,
    model_type: str,
):
    pretty_print_lp(problem, model_type)
    D, A, b, tspan, name, test_points, D_testing_points = problem

    D = torch.tensor(D, dtype=torch.float32, device=device)
    A = torch.tensor(A, dtype=torch.float32, device=device)
    b = torch.tensor(b, dtype=torch.float32, device=device)
    solutions = []
    objective = createObjectiveFun(D)
    for case in cases:
        model, loss_list, mov_list = train_model(
            A,
            b,
            D,
            f"{name} (CASE {case})",
            tspan,
            case,
            epochs,
            batch_size,
            batches,
            device,
            model_type=model_type,
        )

        if (case in [1, 2] and test_points is not None) or (
            case == 3 and D_testing_points is not None
        ):
            test_points = (
                ([D.tolist()] if D_testing_points is None else D_testing_points)
                if case == 3
                else test_points
            )
            test_model(model, device, test_points, case, tspan[1], objective)

        if saving_dir is not None:
            filename = get_file_name(
                epochs, case, name=name, dir_name=saving_dir, model_type=model_type
            )
            save_model(model, filename)
            save_lists_to_file(loss_list, mov_list, filename)
            movs_filename = f"{filename}_mov.txt"
            loss_filename = f"{filename}_loss.txt"

            if do_plot:
                plot_data(loss_filename, "Trainig Loss", "Loss")
                plot_data(movs_filename, "Trainig MOV", "MOV")
        if case == 1:
            t_tensor = torch.tensor(
                tspan[1], dtype=torch.float32, device=device, requires_grad=True
            )
        elif case == 2:
            t_tensor = torch.tensor(
                [tspan[1], *b], dtype=torch.float32, device=device, requires_grad=True
            ).unsqueeze(0)
        else:
            t_tensor = torch.tensor(
                [tspan[1], *D], dtype=torch.float32, device=device, requires_grad=True
            ).unsqueeze(0)
        y_pred = model(t_tensor)
        y_pred_np = y_pred.cpu().detach().numpy()
        sol = Solution(y_pred_np, model, loss_list, mov_list)

        solutions.append(sol)
    return solutions


def train(
    *,
    batches: int = 1,
    batch_size: int = 128,
    epochs: int = 1000,
    problem: Problem | None = None,
    problems_ids: List[int] = [1],
    cases: List[int] = [1],
    do_plot: bool = True,
    saving_dir: str | None = None,
    model_type: str = "pinn",
):

    # torch.manual_seed(2025)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    solutions = []
    equality = model_type != "pinn"
    if problem is None:
        problems = get_all_problems()
        for problem_indx in problems_ids:
            problem_fn = problems[problem_indx - 1]
            sols = _train(
                batches,
                batch_size,
                epochs,
                problem_fn(equality=equality),
                cases,
                do_plot,
                saving_dir,
                device,
                model_type,
            )
            solutions = solutions + sols
    else:
        sols = _train(
            batches,
            batch_size,
            epochs,
            problem,
            cases,
            do_plot,
            saving_dir,
            device,
            model_type,
        )
        solutions = solutions + sols

    return solutions


if __name__ == "__main__":
    pass
