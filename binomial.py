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

    # ---- Greeks Calculation (Finite Difference: Works for Euro & American) ----
    dS = max(1.0, S * 0.01)
    dSigma = max(0.01, sigma * 0.02)
    dT = min(1/365, T/50)  # 1 day or smaller for short maturities
    dR = 0.0001

    # Defensive: clamp to positive
    S_up = S + dS
    S_down = max(1e-8, S - dS)
    sigma_up = sigma + dSigma
    sigma_down = max(1e-8, sigma - dSigma)
    T_up = T + dT
    T_down = max(1e-8, T - dT)
    r_up = r + dR
    r_down = r - dR

    # Price for Greeks
    try:
        price_up = binomial_option_pricing(S_up, K, T, r, sigma, steps, option_type, american, q)
        price_down = binomial_option_pricing(S_down, K, T, r, sigma, steps, option_type, american, q)
        delta = (price_up - price_down) / (S_up - S_down)
    except Exception:
        delta = float("nan")

    try:
        price_upup = binomial_option_pricing(S_up, K, T, r, sigma, steps, option_type, american, q)
        price_mid = price
        price_downdown = binomial_option_pricing(S_down, K, T, r, sigma, steps, option_type, american, q)
        gamma = (price_upup - 2 * price_mid + price_downdown) / ((0.5 * (S_up - S_down)) ** 2)
    except Exception:
        gamma = float("nan")

    try:
        price_sigma_up = binomial_option_pricing(S, K, T, r, sigma_up, steps, option_type, american, q)
        price_sigma_down = binomial_option_pricing(S, K, T, r, sigma_down, steps, option_type, american, q)
        vega = (price_sigma_up - price_sigma_down) / (sigma_up - sigma_down)
    except Exception:
        vega = float("nan")

    try:
        price_T_up = binomial_option_pricing(S, K, T_up, r, sigma, steps, option_type, american, q)
        price_T_down = binomial_option_pricing(S, K, T_down, r, sigma, steps, option_type, american, q)
        theta = (price_T_down - price_T_up) / (T_down - T_up)
    except Exception:
        theta = float("nan")

    try:
        price_r_up = binomial_option_pricing(S, K, T, r_up, sigma, steps, option_type, american, q)
        price_r_down = binomial_option_pricing(S, K, T, r_down, sigma, steps, option_type, american, q)
        rho = (price_r_up - price_r_down) / (r_up - r_down)
    except Exception:
        rho = float("nan")

    return price, delta, gamma, vega, theta, rhs