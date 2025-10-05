import numpy as np
from binomial import binomial_option_pricing

from binomial import binomial_option_pricing
import pytest

def test_binomial_call_european():
    price = binomial_option_pricing(100, 100, 1, 0.05, 0.2, 50, "call", american=False)
    assert price > 0

def test_binomial_put_american():
    price = binomial_option_pricing(100, 100, 1, 0.05, 0.2, 50, "put", american=True)
    assert price > 0

def test_binomial_invalid_option_type():
    with pytest.raises(ValueError):
        binomial_option_pricing(100, 100, 1, 0.05, 0.2, 50, "invalidtype")

def test_binomial_call_price():
    price = binomial_option_pricing(100, 100, 1, 0.05, 0.2, 100, "call")
    assert price > 0
def test_pytest_discovery():
    assert True

print("test_binomial.py loaded")  # or "test_greeks.py loaded"
def binomial_option_pricing(
    S, K, T, r, sigma, steps, option_type, american=False, q=0.0, return_greeks=False
):
    steps = int(steps)
    if steps <= 0:
        raise ValueError("Number of steps must be a positive integer.")

    # Handle zero volatility as deterministic payoff
    if sigma == 0:
        discount = np.exp(-r * T)
        if option_type == "call":
            return max(S - K * discount, 0)
        elif option_type == "put":
            return max(K * discount - S, 0)
        else:
            raise ValueError(f"Invalid option_type: {option_type}")

    dt = T / steps
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp((r - q) * dt) - d) / (u - d)

    # Option values at maturity
    option_values = np.zeros(steps + 1)
    for i in range(steps + 1):
        S_T = S * (u ** (steps - i)) * (d ** i)
        if option_type == "call":
            option_values[i] = max(S_T - K, 0)
        elif option_type == "put":
            option_values[i] = max(K - S_T, 0)
        else:
            raise ValueError(f"Invalid option_type: {option_type}")

    # Backward induction
    for j in range(steps - 1, -1, -1):
        for i in range(j + 1):
            option_values[i] = np.exp(-r * dt) * (
                p * option_values[i] + (1 - p) * option_values[i + 1]
            )
            if american:
                S_t = S * (u ** (j - i)) * (d ** i)
                if option_type == "call":
                    option_values[i] = max(option_values[i], S_t - K)
                elif option_type == "put":
                    option_values[i] = max(option_values[i], K - S_t)
    # Only price is returned. Add Greeks calculation if needed.
    return option_values[0]