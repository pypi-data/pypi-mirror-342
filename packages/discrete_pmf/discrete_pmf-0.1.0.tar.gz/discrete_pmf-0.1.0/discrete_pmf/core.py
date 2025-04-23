import math
import matplotlib.pyplot as plt

def binom_pmf(x_values, n, p_list, plot=True):
"""
   Description:
   ------------
    binom_pmf: compute and optionally plot the Binomial probability mass function.

    Args:
   ------
        x_values (list[int]): Values of the random variable X (e.g., [0, 1, 2, ..., n]).
        n (int): Number of trials.
        p_list (list[float]): A list of probabilities of success (0 < p < 1).
        plot (bool): If True, plots the PMF using matplotlib.

    Returns:
   ---------
        dict: Dictionary mapping each p to a list of PMF values at the given x_values.

	from discrete_pmf import p_binom

	=======Example=======

	x = list(range(0, 6))
        p = [0.3, 0.7]
	binom_pmf(x_values=x, n=5, p_list=p)

    """

    results = {}
    colors = plt.cm.viridis_r  # Choose a preferred colormap

    if plot:
        plt.figure(figsize=(8, 5))

    for i, p in enumerate(p_list):
        result = []
        for x in x_values:
            binomial = math.comb(n, x) * (p ** x) * ((1 - p) ** (n - x))
            result.append(round(binomial, 5))
        results[p] = result

        if plot:
            color = colors(i / max(len(p_list) - 1, 1)) 
            markerline, stemlines, baseline = plt.stem(
                x_values,
                result,
                label=f"p={p}",
                basefmt=" ",
            )
            plt.setp(markerline, color=color)
            plt.setp(stemlines, color=color)

    if plot:
        plt.title(f"Binomial PMF (n={n}, p={p_list})")
        plt.xlabel("x")
        plt.ylabel("P(X = x)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    return results 



def geom_pmf(x_values, p_list, plot=True):
"""
    Description:
    ------------
    geom_pmf: compute and optionally plot the Geometric probability mass function.

    Args:
    ------
        x_values (list[int]): Values of the random variable X (must start from 1).
        p_list (list[float]): A list of probabilities of success (0 < p < 1).
        plot (bool): If True, plots the PMF using matplotlib.

    Returns:
    ---------
        dict: Dictionary mapping each p to a list of PMF values at the given x_values.

        from discrete_pmf import p_geom

        =======Example=======

        x = list(range(1, 8))
        p = [0.3, 0.5]
        geom_pmf(x_values=x, p_list=p)
"""

    results = {}
    colors = plt.cm.viridis_r  # Choose a good colormap

    if plot:
        plt.figure(figsize=(8, 5))

    for i, p in enumerate(p_list):
        result = []
        for x in x_values:
            if x == 0:
                print("The random variable 'X' cannot contain 0 values. Check the list of x_values")
                return
            else:
                geometric = (1-p) ** (x-1) * p
                result.append(round(geometric, 5))
            results[p] = result

        if plot:
            color = colors(i / max(len(p_list) - 1, 1))  
            markerline, stemlines, baseline = plt.stem(
                x_values,
                result,
                label=f"p={p}",
                basefmt=" ",
            )
            plt.setp(markerline, color=color)
            plt.setp(stemlines, color=color)

    if plot:
        plt.title(f"Geometric PMF (Number of x={len(x_values)})")
        plt.xlabel("x")
        plt.ylabel("P(X = x)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    return results


def neg_binom_pmf(x_values, r, p_list, plot=True):
"""
    Description:
    ------------
    neg_binom_pmf: compute and optionally plot the Negative Binomial probability mass function.

    Args:
    ------
        x_values (list[int]): Values of the random variable X (e.g., number of trials until r successes).
        r (int): Number of required successes.
        p_list (list[float]): A list of probabilities of success (0 < p < 1).
        plot (bool): If True, plots the PMF using matplotlib.

    Returns:
    ---------
        dict: Dictionary mapping each p to a list of PMF values at the given x_values.

        from discrete_pmf import p_neg_binom

        =======Example=======

        x = list(range(5, 15))
        p = [0.3, 0.5]
        r = 5
        neg_binom_pmf(x_values=x, r=r, p_list=p)
"""

    results = {}
    colors = plt.cm.viridis_r  # Choose a good colormap

    if plot:
        plt.figure(figsize=(8, 5))

    for i, p in enumerate(p_list):
        result = []
        for x in x_values:
                if x > r:
                    neg_binomial = math.comb(x-1, r-1)*((1-p)**(x-r))*(p**r)
                
                else:
                    neg_binomial = 0
                    
                result.append(round(neg_binomial, 5))
                results[p] = result

        if plot:
            color = colors(i / max(len(p_list) - 1, 1))  # Handle 1-element case
            markerline, stemlines, baseline = plt.stem(
                x_values,
                result,
                label=f"p={p}",
                basefmt=" ",
            )
            plt.setp(markerline, color=color)
            plt.setp(stemlines, color=color)

    if plot:
        plt.title(f"Negative Binomial PMF (r={r})(p={p_list})")
        plt.xlabel("x")
        plt.ylabel("P(X = x)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    return results


def poisson_pmf(x_values, lmd_list , plot=True):
"""
    Description:
    ------------
    poisson_pmf: compute and optionally plot the Poisson probability mass function.

    Args:
    ------
        x_values (list[int]): Values of the random variable X (non-negative integers).
        lmd_list (list[float]): A list of lambda (rate) values.
        plot (bool): If True, plots the PMF using matplotlib.

    Returns:
    ---------
        dict: Dictionary mapping each λ to a list of PMF values at the given x_values.

        from discrete_pmf import p_poisson

        =======Example=======

        x = list(range(0, 10))
        lambdas = [2, 5]
        poisson_pmf(x_values=x, lmd_list=lambdas)
"""

    results = {}
    colors = plt.cm.viridis_r  # Choose a good colormap

    if plot:
        plt.figure(figsize=(8, 5))

    for i, lmd in enumerate(lmd_list):
        result = []
        for x in x_values:
            poisson = (math.exp(-lmd) * (lmd ** x)) / math.factorial(x)
            result.append(round(poisson, 5))
            
        results[lmd] = result

        if plot:
            color = colors(i / max(len(lmd_list) - 1, 1))  # Handle 1-element case
            markerline, stemlines, baseline = plt.stem(
                x_values,
                result,
                label=f"λ ={lmd}",
                basefmt=" ",
            )
            plt.setp(markerline, color=color)
            plt.setp(stemlines, color=color)

    if plot:
        plt.title(f"Poisson PMF (λ = {lmd_list})")
        plt.xlabel("x")
        plt.ylabel("P(X = x)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    return results
