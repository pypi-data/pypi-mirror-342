import argparse
import os
from time import sleep

import torch

from .train import train
from .models import load_model
from .ode import createPhi
from .problems import problem1, problem2


def main():
    parser = argparse.ArgumentParser(
        description="Train the PINN model using named arguments"
    )
    parser.add_argument("--no-action", help="No action needed", action="store_true")

    parser.add_argument(
        "--iterations", type=int, default=1000, help="Number of training iterations"
    )

    parser.add_argument(
        "--batches", type=int, default=1, help="Number of training batches"
    )
    parser.add_argument("--batch_size", type=int, default=128, help="Batch size")
    parser.add_argument(
        "--model",
        type=str,
        choices=["pinn", "rnn"],
        default="pinn",
        help="Model use pinn for Ax<= b, use rnn for Ax=b, x>=0 ",
    )

    parser.add_argument(
        "--folder",
        "-f",
        type=str,
        help="Path to the saving folder",
        # action="store_const",
        # const=None,
    )
    parser.add_argument(
        "--load",
        "-l",
        type=str,
        help="Path to model file",
        # action="store_const",
        # const=None,
    )
    parser.add_argument(
        "--in_dim",
        "-in",
        type=int,
        # action="store_const",
        # const=None,
        help="Number of Input Variables.",
    )
    parser.add_argument(
        "--out_dim",
        "-out",
        type=int,
        # action="store_const",
        # const=None,
        help="Number of Output Variables.",
    )
    parser.add_argument(
        "--T",
        "-T",
        type=float,
        # action="store_const",
        # const=None,
        help="Upper limit of the time interval.",
    )
    parser.add_argument("--do_plot", action="store_true", help="Plot them")
    parser.add_argument(
        "--case",
        nargs="+",
        type=int,
        choices=[1, 2, 3],
        default="1",
        help="Which case to run (1: time only, 2: time and b, 3: time and D)",
    )
    parser.add_argument(
        "--example",
        nargs="+",
        type=int,
        choices=[1, 2, 3, 4],
        default=None,
        help="Which example to run (1, 2, 3, ...)",
    )
    args = parser.parse_args()

    if args.no_action:
        print("No action flag is set.")
        # read_mps("mps_files/problem2.mps")
        # plot_loss()
        from tqdm import tqdm

        # from tqdm import tqdm_notebook

        rnag1 = tqdm(range(2), desc="Outer loop")
        rnag2 = tqdm(range(2), desc="Inner loop", leave=False)
        # else:
        #         rnag1 = tqdm(range(10), desc="Outer loop")
        #         rnag2 = tqdm(range(20), desc="Inner loop", leave=False)

        for i in rnag1:
            # Inner loop; using leave=False so it doesn't keep each inner bar on a new line
            for j in rnag2:
                # Simulate some work
                sleep(0.01)
        D, A, b, tspan, name, test_points, D_testing_points = problem1(equality=False)
        D = torch.tensor(D, dtype=torch.float32)
        A = torch.tensor(A, dtype=torch.float32)
        b = torch.tensor(b, dtype=torch.float32)
        # print(D)
        print(A.shape)
        # print(b)
        models = [("pinn", sum(A.shape)), ("rnn", sum(D.shape) + sum(A.shape))]
        for m, sz in models:
            phi, dim = createPhi(D, A, model=m)(b), sz
            y1 = torch.ones(dim, dtype=torch.float32)
            y2 = torch.ones((5, dim), dtype=torch.float32)
            val1 = phi(y1)
            print(f"Model: {m}\n")
            print(f"dim y1 = {y1.shape}\n", val1)
            val2 = phi(y2)
            print(f"dim y2 = {y2.shape}\n", val2)

        exit(0)
    # examples = [example_1, example_2, example_3]
    if args.load:
        filename = args.load
        assert (
            args.in_dim is not None and args.out_dim is not None
        ), "You must provide the number of variables in and out."
        assert os.path.exists(filename), "The file does not exist; check the name."
        print(f"Loading file {filename}")
        T = 10.0 if args.T is None else args.T
        val = load_model(args.load, args.in_dim, args.out_dim, model_type=args.model)(T)
        print(val)

        exit(0)
    print(f"Running example {args.example} for {args.iterations} epochs.")
    train(
        batches=args.batches,
        batch_size=args.batch_size,
        epochs=args.iterations,
        cases=args.case,
        problems_ids=args.example,
        do_plot=args.do_plot,
        saving_dir=args.folder,
        model_type=args.model,
    )


if __name__ == "__main__":
    main()
