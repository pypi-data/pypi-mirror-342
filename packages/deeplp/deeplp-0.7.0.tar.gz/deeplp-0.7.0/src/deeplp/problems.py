from collections import namedtuple
from typing import List, Tuple

from deeplp.utils import cutename


Problem = namedtuple(
    "Problem",
    ["D", "A", "b", "tspan", "name", "b_testing_points", "c_testing_points"],
    defaults=[None],
)


def createProblem(
    c: List[float],
    A: List[List[float]],
    b: List[float],
    tspan: Tuple[float, float],
    *,
    name: str | None = None,
    b_testing_points: List[List[float]] | None = None,
    c_testing_points: List[List[float]] | None = None,
):
    name = cutename() if name is None else name
    return Problem(
        c,
        A,
        b,
        tspan,
        name=name,
        b_testing_points=b_testing_points,
        c_testing_points=c_testing_points,
    )


def problem1(*, equality=False):
    name = "Example 1"
    if equality:
        d = [-9.54, -8.16, -4.26, -11.43]
        D = [*d, *(map(lambda x: -x, d)), 0.0]
        a = [3.18, 2.72, 1.42, 3.81]
        A = [[*a, *(map(lambda x: -x, a)), 1.0]]
        b = [7.81]
        c1 = [-29.99, -25.66, -13.39, -35.94]
        c2 = [-3.87, -3.31, -1.73, -4.63]
        c3 = [-24.65, -21.09, -11.01, -29.54]
        c_testing_points = [
            [*c1, *(map(lambda x: -x, c1)), 0],
            [*c2, *(map(lambda x: -x, c2)), 0],
            [*c3, *(map(lambda x: -x, c3)), 0],
        ]
    else:
        D = [-9.54, -8.16, -4.26, -11.43]
        A = [[3.18, 2.72, 1.42, 3.81]]
        b = [7.81]
        c_testing_points = [
            [-29.99, -25.66, -13.39, -35.94],
            [-3.87, -3.31, -1.73, -4.63],
            [-24.65, -21.09, -11.01, -29.54],
        ]
    test_points = [[8.16], [6.72], [6.18]]
    tspan = (0.0, 10.0)
    return Problem(
        D,
        A,
        b,
        tspan,
        name,
        test_points,
        c_testing_points,
    )


# Example 1. page 48 (62): Linear and Nonlinear
def problem2(*, equality=False):
    name = "Example 2"
    if equality:
        D = [-3, -1, -3]
        A = [[2, 1, 1], [1, 2, 3], [2, 2, 1]]
        b = [2, 5, 6]
        c_testing_points = [D]
    else:
        D = [-3, -1, -3]
        A = [[2, 1, 1], [1, 2, 3], [2, 2, 1], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]
        b = [2, 5, 6, 0, 0, 0]
        c_testing_points = [D]

    tspan = (0.0, 30.0)
    return Problem(D, A, b, tspan, name, [b], c_testing_points)


def problem3(*, equality=False):
    name = "Example 3"
    D = [-1.0, -4.0, -3.0]
    A = [
        [2.0, 2.0, 1.0],  # 2x1 + 2x2 + x3 <= 4
        [1.0, 2.0, 2.0],  # x1 + 2x2 + 2x3 <= 6
        [-1.0, 0.0, 0.0],  # -x1 <= 0
        [0.0, -1.0, 0.0],  # -x2 <= 0
        [0.0, 0.0, -1.0],  # -x3 <= 0
    ]
    b = [4.0, 6.0, 0.0, 0.0, 0.0]
    tspan = (0.0, 50.0)
    return Problem(D, A, b, tspan, name, [b])


def problem4(*, equality=False):
    name = "Example 4"
    b = [15, 21, 27, 45, 30]
    A = [[3, -5], [3, -1], [3, 1], [3, 4], [1, 3]]
    D = [[-1, -2], [-2, -1]]
    tspan = (0.0, 20)
    return Problem(D[0], A, b, tspan, name, [b])


def pretty_print_lp(problem, model_type):
    """
    Pretty-prints a linear program defined by a Problem namedtuple with fields:
      D : coefficients for the objective function (list or array)
      A : constraint matrix (list of lists or 2D array)
      b : right-hand side values (list)
      name : problem name (string)
    """
    name = problem.name
    D = problem.D
    A = problem.A
    b = problem.b

    # Build objective string:
    # For example, if D = [-1, -2], we want: "-1*x1 - 2*x2"
    obj_terms = []
    for i, coef in enumerate(D):
        # Format coefficient, avoiding a leading "+" for negative numbers.
        # We convert coef to string and then add *xi.
        term = f"{coef}*x{i+1}"
        obj_terms.append(term)
    objective_str = " + ".join(obj_terms)
    # Replace occurrences of "+ -" with "- " for nicer formatting.
    objective_str = objective_str.replace("+ -", "- ")

    # Build constraint strings:
    constraint_strs = []
    op = "<=" if model_type == "pinn" else "="
    for row, bound in zip(A, b):
        row_terms = []
        for j, coef in enumerate(row):
            term = f"{coef}*x{j+1}"
            row_terms.append(term)
        constr = " + ".join(row_terms)
        constr = constr.replace("+ -", "- ")
        constr += f" {op} {bound}"
        constraint_strs.append(constr)
    nonneg_constraints = [f"x{i+1} >= 0" for i in range(len(D))]
    # Print the full linear program:
    print(f"Linear Program: {name}")
    print("Minimize:")
    print("   ", objective_str)
    print("Subject to:")
    for cs in constraint_strs:
        print("   ", cs)
    if model_type != "pinn":
        for nn in nonneg_constraints:
            print("   ", nn)


def get_all_problems():
    return [problem1, problem2, problem3, problem4]
