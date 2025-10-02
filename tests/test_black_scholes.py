from black_scholes import black_scholes_price

def test_black_scholes_call():
    price = black_scholes_price("call", 100, 100, 1, 0.05, 0.2)
    assert abs(price - 10.45) < 0.2

def test_black_scholes_put():
    price = black_scholes_price("put", 100, 100, 1, 0.05, 0.2)
    assert abs(price - 5.57) < 0.2