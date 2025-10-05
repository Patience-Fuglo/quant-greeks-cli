from math import exp, sqrt, isclose
def binomial_option_pricing(
    S, K, T, r, sigma, steps, option_type, american=False, q=0.0, return_greeks=False
):
    steps = int(steps)
    if steps <= 0:
        raise ValueError("Number of steps must be a positive integer.")

    dt = T / steps
    u = exp(sigma * sqrt(dt))
    d = 1 / u
    p = (exp((r - q) * dt) - d) / (u - d)

    # Build asset prices at maturity
    prices = [S * (u ** j) * (d ** (steps - j)) for j in range(steps + 1)]
    # Option value at maturity
    if option_type == "call":
        values = [max(price - K, 0) for price in prices]
    else:
        values = [max(K - price, 0) for price in prices]

    value_tree = [values[:]]
    price_tree = [prices[:]]

    for i in range(steps - 1, -1, -1):
        prices = [prices[j] / u for j in range(i + 1)]
        new_values = []
        for j in range(i + 1):
            hold = exp(-r * dt) * (p * values[j + 1] + (1 - p) * values[j])
            if option_type == "call":
                exercise = max(prices[j] - K, 0)
            else:
                exercise = max(K - prices[j], 0)
            if american:
                new_values.append(max(hold, exercise))
            else:
                new_values.append(hold)
        values = new_values
        value_tree.insert(0, values[:])
        price_tree.insert(0, prices[:])

    price = values[0]

    if not return_greeks:
        return price

    # For American options, set Greeks to nan for now
    if american:
        nan = float("nan")
        return price, nan, nan, nan, nan, nan

    # ---- Greeks Calculation (European only) ----
    # Clamp finite difference steps
    dS = 1.0
    dSigma = 0.01
    dT = 1/365  # 1 day
    dR = 0.0001

    # Delta
    S_up, S_down = S + dS, S - dS
    try:
        price_up = binomial_option_pricing(S_up, K, T, r, sigma, steps, option_type, american, q)
        price_down = binomial_option_pricing(S_down, K, T, r, sigma, steps, option_type, american, q)
        delta = (price_up - price_down) / (2 * dS) if not isclose(S_up, S_down) else float("nan")
    except Exception:
        delta = float("nan")

    # Gamma
    try:
        price_upup = binomial_option_pricing(S + dS, K, T, r, sigma, steps, option_type, american, q)
        price = binomial_option_pricing(S, K, T, r, sigma, steps, option_type, american, q)
        price_downdown = binomial_option_pricing(S - dS, K, T, r, sigma, steps, option_type, american, q)
        gamma = (price_upup - 2 * price + price_downdown) / (dS ** 2)
    except Exception:
        gamma = float("nan")

    # Vega (w.r.t. sigma)
    try:
        price_sigma_up = binomial_option_pricing(S, K, T, r, sigma + dSigma, steps, option_type, american, q)
        price_sigma_down = binomial_option_pricing(S, K, T, r, sigma - dSigma, steps, option_type, american, q)
        vega = (price_sigma_up - price_sigma_down) / (2 * dSigma)
    except Exception:
        vega = float("nan")

    # Theta (w.r.t. T)
    try:
        T_up = max(T + dT, 1e-8)
        T_down = max(T - dT, 1e-8)
        price_T_up = binomial_option_pricing(S, K, T_up, r, sigma, steps, option_type, american, q)
        price_T_down = binomial_option_pricing(S, K, T_down, r, sigma, steps, option_type, american, q)
        theta = (price_T_down - price_T_up) / (2 * dT)
    except Exception:
        theta = float("nan")

    # Rho (w.r.t. r)
    try:
        price_r_up = binomial_option_pricing(S, K, T, r + dR, sigma, steps, option_type, american, q)
        price_r_down = binomial_option_pricing(S, K, T, r - dR, sigma, steps, option_type, american, q)
        rho = (price_r_up - price_r_down) / (2 * dR)
    except Exception:
        rho = float("nan")

    return price, delta, gamma, vega, theta, rho