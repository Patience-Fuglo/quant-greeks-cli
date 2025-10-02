import math
from scipy.stats import norm

def black_scholes_price(option_type, S, K, T, r, sigma, q=0.0):
    """
    Calculate Black-Scholes price for European options with continuous dividend yield.
    option_type: "call" or "put"
    S: Current stock price
    K: Strike price
    T: Time to expiry (in years)
    r: Risk-free rate
    sigma: Volatility
    q: Continuous dividend yield (default 0)
    """
    if T <= 0 or sigma <= 0:
        return max(0.0, S - K) if option_type == "call" else max(0.0, K - S)
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if option_type == "call":
        price = S * math.exp(-q * T) * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        price = K * math.exp(-r * T) * norm.cdf(-d2) - S * math.exp(-q * T) * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")
    return price