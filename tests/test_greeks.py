import math
from scipy.stats import norm
from greeks import delta


from greeks import delta, gamma, vega, theta, rho
import pytest

def test_delta_call_and_put():
    assert -1 <= delta("call", 100, 100, 1, 0.05, 0.2) <= 1
    assert -1 <= delta("put", 100, 100, 1, 0.05, 0.2) <= 1

def test_greeks_zero_volatility():
    assert gamma("call", 100, 100, 1, 0.05, 0.0) == 0
    assert vega("call", 100, 100, 1, 0.05, 0.0) == 0
    assert theta("call", 100, 100, 1, 0.05, 0.0) == 0
    assert rho("call", 100, 100, 1, 0.05, 0.0) == 0

def test_greeks_invalid_option_type():
    with pytest.raises(ValueError):
        delta("invalid", 100, 100, 1, 0.05, 0.2)
def test_delta_call():
    d = delta("call", 100, 100, 1, 0.05, 0.2)
    assert abs(d) <= 1
def test_pytest_discovery():
    assert True

print("test_binomial.py loaded")  # or "test_greeks.py loaded"

def delta(option_type, S, K, T, r, sigma, q=0.0):
    if sigma == 0:
        return 0.0
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    if option_type == "call":
        return math.exp(-q * T) * norm.cdf(d1)
    elif option_type == "put":
        return -math.exp(-q * T) * norm.cdf(-d1)
    else:
        raise ValueError(f"Invalid option_type: {option_type}")

def gamma(option_type, S, K, T, r, sigma, q=0.0):
    if sigma == 0:
        return 0.0
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    return math.exp(-q * T) * norm.pdf(d1) / (S * sigma * math.sqrt(T))

def vega(option_type, S, K, T, r, sigma, q=0.0):
    if sigma == 0:
        return 0.0
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    return S * math.exp(-q * T) * norm.pdf(d1) * math.sqrt(T) / 100

def theta(option_type, S, K, T, r, sigma, q=0.0):
    if sigma == 0:
        return 0.0
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if option_type == "call":
        return (
            - (S * norm.pdf(d1) * sigma * math.exp(-q * T)) / (2 * math.sqrt(T))
            - r * K * math.exp(-r * T) * norm.cdf(d2)
            + q * S * math.exp(-q * T) * norm.cdf(d1)
        ) / 365
    elif option_type == "put":
        return (
            - (S * norm.pdf(d1) * sigma * math.exp(-q * T)) / (2 * math.sqrt(T))
            + r * K * math.exp(-r * T) * norm.cdf(-d2)
            - q * S * math.exp(-q * T) * norm.cdf(-d1)
        ) / 365
    else:
        raise ValueError(f"Invalid option_type: {option_type}")

def rho(option_type, S, K, T, r, sigma, q=0.0):
    if sigma == 0:
        return 0.0
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if option_type == "call":
        return K * T * math.exp(-r * T) * norm.cdf(d2) / 100
    elif option_type == "put":
        return -K * T * math.exp(-r * T) * norm.cdf(-d2) / 100
    else:
        raise ValueError(f"Invalid option_type: {option_type}")