import datetime
import os
import random
import pulp
import torch
import numpy as np

# from IPython import get_ipython

adjectives = [
    "groundbreaking",
    "revolutionary",
    "important",
    "novel",
    "fun",
    "interesting",
    "fascinating",
    "exciting",
    "surprising",
    "remarkable",
    "wonderful",
    "stunning",
    "mini",
    "small",
    "tiny",
    "cute",
    "friendly",
    "wild",
]

nouns = [
    "discovery",
    "experiment",
    "story",
    "journal",
    "notebook",
    "revelation",
    "computation",
    "creation",
    "analysis",
    "invention",
    "blueprint",
    "report",
    "science",
    "magic",
    "program",
    "notes",
    "lecture",
    "theory",
    "proof",
    "conjecture",
]


def cutename():
    """
    Generate a filename like "Cute discovery". Does not end with an extension.
    """
    adjective = random.choice(adjectives).title()  # Convert to title case
    noun = random.choice(nouns)
    return f"{adjective} {noun}"


# Load the MPS file into a PuLP model.
# This assumes your MPS file (e.g. "problem.mps") is formatted correctly.
def read_mps(filename: str):
    # Load the MPS file into a PuLP model.
    # This assumes your MPS file (e.g. "problem.mps") is formatted correctly.
    variables, prob = pulp.LpProblem.fromMPS(filename)
    print(prob)
    print(prob.objective.to_dict())
    # Get the list of variables (the order will be used for constructing matrices)
    var_names = list(map(lambda v: v, variables))
    n = len(variables)

    # --- Extract Objective ---
    # Use map to extract coefficients for each variable (defaulting to 0 if missing)
    obj_coeffs = list(map(lambda v: v["value"], prob.objective.to_dict()))

    # Convert to a NumPy array and then to a torch tensor.
    obj_np = np.array(obj_coeffs, dtype=np.float32)
    obj_tensor = torch.tensor(obj_np, dtype=torch.float32)
    print("Objective tensor:")
    print(obj_tensor)

    # --- Extract Constraints ---
    def extract_constraint(cons):
        # Build a row of zeros for the coefficients corresponding to each variable.
        row = [0.0] * n
        # cons is an LpConstraint (an LpAffineExpression): its items provide (variable, coefficient) pairs.
        for var, coeff in cons.items():
            # Use var_names.index(var.name) to locate the index for this variable.
            idx = var_names.index(var.name)
            row[idx] = coeff
        # The right-hand side is defined as -constant.
        return row, -cons.constant

    # Use map to process all constraints.
    rows_b = list(map(extract_constraint, prob.constraints.values()))
    A_rows = [row for row, b_val in rows_b]
    b_rows = [b_val for row, b_val in rows_b]

    # Convert A and b to NumPy arrays and then torch tensors.
    A_np = np.array(A_rows, dtype=np.float32)
    b_np = np.array(b_rows, dtype=np.float32)
    A_tensor = torch.tensor(A_np, dtype=torch.float32)
    b_tensor = torch.tensor(b_np, dtype=torch.float32)

    print("Constraint matrix A:")
    print(A_tensor)
    print("Right-hand side b:")
    print(b_tensor)


def is_notebook():
    try:
        from IPython import get_ipython

        if "IPKernelApp" not in get_ipython().config:  # pragma: no cover
            # raise ImportError("console")
            return False
        if "VSCODE_PID" in os.environ:  # pragma: no cover
            # raise ImportError("vscode")
            return True
    except:
        return False
    else:  # pragma: no cover
        return True


def get_file_name(
    epochs,
    case,
    *,
    name: str = "",
    dir_name: str = "saved_models",
    model_type: str = "pinn",
):
    case_saving_dir = f"{dir_name}/case_{case}"
    os.makedirs(case_saving_dir, exist_ok=True)
    current_date = datetime.date.today().strftime("%Y_%m_%d")
    name = name.lower().replace(" ", "_")
    filename = f"{case_saving_dir}/{name}"
    if case == 1:
        filename = f"{filename}_time_only_{model_type}_{epochs}"
    elif case == 2:
        filename = f"{filename}_time_and_b_{model_type}_{epochs}"
    else:
        filename = f"{filename}_time_and_D_{model_type}_{epochs}"

    return f"{filename}_{current_date}"
