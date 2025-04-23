# Discrete PMF — Python Module for Plotting PMFs of Discrete Distributions

**Discrete PMF** is a lightweight and easy-to-use Python module for computing and visualizing **Probability Mass Functions (PMFs)** of common discrete probability distributions. It is ideal for educators, data scientists, statisticians, and learners who want to visualize and interact with probability distributions in Python.

---

## Supported Distributions

- **Binomial Distribution**
- **Geometric Distribution**
- **Negative Binomial Distribution**
- **Poisson Distribution**

Each function:
- Computes the PMF for a given distribution
- Optionally generates a matplotlib stem plot
- Returns the PMF values as a dictionary for further processing

---

## Requirements

- **Python ≥ 3.6**
- **matplotlib** (for plotting)
- Standard Library: `math`

Install dependencies with:

```bash
pip install matplotlib
```

Or if you're using [Poetry](https://python-poetry.org/):

```bash
poetry add matplotlib
```


## Function Overview

### 🔹 `binom_pmf(x_values, n, p_list, plot=True)`
Compute and (optionally) plot the **Binomial** PMF.

**Parameters:**
- `x_values (List[int])`: Values of the random variable X (e.g., [0, 1, 2, ..., n])
- `n (int)`: Number of trials
- `p_list (List[float])`: List of success probabilities (e.g., [0.3, 0.7])
- `plot (bool)`: If True, displays a matplotlib stem plot (default: `True`)

**Returns:**
- `Dict[float, List[float]]`: Mapping from each `p` to its list of PMF values.

**Example:**
```python
from discrete_pmf import binom_pmf

x = list(range(0, 6))
n = 5
p_values = [0.3, 0.7]

binom_pmf(x_values=x, n=n, p_list=p_values, plot=True)
```


## 📚 Documentation

Each function includes Python docstrings explaining:
- Function purpose
- Parameters and types
- Return values
- Example usage


---


## 📝 License

MIT License. See `LICENSE` file for details.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change or add.


