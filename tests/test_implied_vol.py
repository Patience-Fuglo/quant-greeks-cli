from implied_vol import implied_volatility

def test_implied_vol_call():
    sigma = implied_volatility("call", 100, 100, 1, 0.05, 10.45)
    assert abs(sigma - 0.2) < 0.05