# import numpy as np
# from scipy.optimize import linprog
# from scipy.integrate import solve_ivp
# import torch

# from .ode import createPhi


# def solve_lp(D, A, b):
#     res = linprog(D, A_ub=A, b_ub=b, bounds=(None, None), method="highs")
#     assert res.success, "Solver found no solution"
#     return res.x, res.fun


# def solve_ode(problem):
#     D, A, b, tspan, _, _, _ = problem
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     D = torch.tensor(D, dtype=torch.float32, device=device)
#     A = torch.tensor(A, dtype=torch.float32, device=device)
#     b = torch.tensor(b, dtype=torch.float32, device=device)
#     phi = createPhi(D, A)(b)

#     def f(t, y):
#         y = torch.tensor(y, dtype=torch.float32, device=device)
#         y_hat = phi(y)
#         y_hat = y_hat.cpu().detach().numpy()
#         return y_hat

#     # Initial condition
#     t0 = 0.0  # start time
#     y0 = torch.zeros(sum(A.shape), dtype=torch.float32)

#     # Define the time span for the solution

#     # Optionally, specify time points where you want the solution
#     t_eval = np.linspace(t0, tspan[1], 100)

#     # Solve the IVP using RK45 (default method of solve_ivp)
#     solution = solve_ivp(f, tspan, y0, method="RK45", t_eval=t_eval)
#     return solution
