# deeplp

[![PyPI version](https://img.shields.io/pypi/v/deeplp.svg)](https://pypi.org/project/deeplp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
<!-- [![Build Status](https://github.com/yourusername/deeplp/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/deeplp/actions) -->

**deeplp** is a Python package for solving linear programming problems using deep learning techniques. It leverages PyTorch for its backend computations and provides a simple API for defining problems and training models.

## Features

- Define linear programming problems with a simple API.
- Train deep learning models to solve LPs.
- Built-in support for plotting results and saving models.
- A command-line interface (CLI) for running experiments.
- Available on [PyPI](https://pypi.org/project/deeplp) for easy installation.

## Requirements

**deeplp** requires:
- Python 3.10+
- PyTorch (with GPU support if desired)

### Installing PyTorch

Visit the [PyTorch website](https://pytorch.org/get-started/locally/) for installation instructions. For example, to install PyTorch with CUDA 11.3 support on Windows:

```bash
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
```

For CPU-only support, run:

```bash
pip install torch torchvision torchaudio
```

## Installation

You can install **deeplp** either from PyPI or directly from GitHub.

### Installing from PyPI

```bash
pip install deeplp
```

### Installing from GitHub

```bash
pip install git+https://github.com/yourusername/deeplp.git
```

## Basic Usage

### Example 1: Solving a Simple LP

```python
from deeplp import train, createProblem

# Define your problem data:
c = [1.0, 2.0]  # Objective coefficients
A = [[3, -5], [3, -1], [3, 1], [3, 4], [1, 3]]  # Constraint matrix
b = [15, 21, 27, 45, 30]  # Right-hand side values
tspan = (0.0, 10.0)  # Time span

# Create the problem (if no name is provided, a name is generated automatically)
problem = createProblem(
    c,
    A,
    b,
    tspan,
    name="Custom Example 1",
    b_testing_points=[[15, 21, 27, 45, 30], [15, 12, 20, 25, 50]],
    c_testing_points=[[2, 5], [12, 20]],
)

# Train the model
sols = train(
    batches=1,
    batch_size=32,
    epochs=100,
    problem=problem,
    problems_ids=[],
    cases=[1, 2, 3],
    do_plot=True,
    model_type="pinn",
)
```

### Example 2: Solving an LP with Equality Constraints

```python
from deeplp import train, createProblem

# Define your problem data:
c = [1.0, 2.0, -1.0, -2.0, 0, 0, 0, 0, 0]  # Objective coefficients
A = [
    [3, -5, -3, 5, 1, 0, 0, 0, 0],
    [3, -1, -3, 1, 0, 1, 0, 0, 0],
    [3, 1, -3, -1, 0, 0, 1, 0, 0],
    [3, 4, -3, -4, 0, 0, 0, 1, 0],
    [1, 3, -1, -3, 0, 0, 0, 0, 1],
]  # Constraint matrix
b = [15, 21, 27, 45, 30]  # Right-hand side values
tspan = (0.0, 10.0)  # Time span

# Create the problem
problem = createProblem(
    c,
    A,
    b,
    tspan,
    name="Custom Example 2 (Equality)",
    b_testing_points=[[15, 21, 27, 45, 30], [15, 12, 20, 25, 50]],
    c_testing_points=[c],
)

# Train the model
sols = train(
    batches=1,
    batch_size=32,
    epochs=100,
    problem=problem,
    problems_ids=[],
    cases=[3],
    do_plot=True,
    model_type="rnn",
)
```

## Running the CLI

After installing the package, you can run:

```bash
deeplp --batches 1 --batch_size 128 --iterations 1000 --case 1 --example 1 --do_plot --folder saved_models
```

For other options, type 
```bash
python deeplp --help
```

This command starts training with the specified options using the **RNN model** for **case 3, example 2**, with **2 iterations**, **2 batches**, and a batch size of **1**.
