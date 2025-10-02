import math
from scipy.optimize import brentq
from black_scholes import black_scholes_price  # Make sure you have this function in black_scholes.py

def implied_volatility(option_type, S, K, T, r, price, tol=1e-6, max_iterations=100):
    """
    Calculate implied volatility for a European option using the Black-Scholes model.
    """
    def objective(sigma):
        return black_scholes_price(option_type, S, K, T, r, sigma) - price

    try:
        # Implied vol must be positive; market vols are < 500%
        imp_vol = brentq(objective, 1e-8, 5.0, maxiter=max_iterations, xtol=tol)
        return imp_vol
    except Exception as e:
        raise RuntimeError(f"Failed to converge to implied volatility: {e}")