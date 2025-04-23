### Discrete_pmf — A Python module for plotting PMFs of discrete distributions
This module provides simple, customizable utilities for computing and visualizing Probability Mass Functions (PMFs) for commonly used discrete distributions:

Binomial

Geometric

Negative Binomial

Poisson

Each function supports plotting using matplotlib, and returns the computed PMF values for programmatic access.

Requirements
Python ≥ 3.6

matplotlib

Standard Library: math

Available Functions
binom_pmf(x_values, n, p_list, plot=True)
Compute and plot the Binomial Probability Mass Function.

Parameters:
x_values (List[int]): List of x-values at which to evaluate the PMF.

n (int): Number of trials.

p_list (List[float]): List of success probabilities to evaluate.

plot (bool, default=True): Whether to display a PMF plot.

Returns:
Dict[float, List[float]]: Dictionary mapping each p to its corresponding PMF values (rounded to 5 decimal places).
