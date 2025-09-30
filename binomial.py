def binomial_option_price(option_type, S, K, T, r, sigma, steps):
    """
    Price a European option using the Cox-Ross-Rubinstein (CRR) binomial model.

    Parameters:
        option_type: "call" or "put"
        S: Current stock price
        K: Strike price
        T: Time to maturity (years)
        r: Risk-free rate (annual, decimal)
        sigma: Volatility (annual, decimal)
        steps: Number of steps in the binomial tree

    Returns:
        option price (float)
    """
    from math import exp, sqrt

    dt = T / steps
    u = exp(sigma * sqrt(dt))
    d = 1 / u
    p = (exp(r * dt) - d) / (u - d)

    # Stock price tree
    prices = [S * (u ** j) * (d ** (steps - j)) for j in range(steps + 1)]
    # Option value at maturity
    if option_type == "call":
        values = [max(price - K, 0) for price in prices]
    else:
        values = [max(K - price, 0) for price in prices]

    # Backward induction
    for i in range(steps - 1, -1, -1):
        values = [exp(-r * dt) * (p * values[j + 1] + (1 - p) * values[j]) for j in range(i + 1)]
    return values[0]