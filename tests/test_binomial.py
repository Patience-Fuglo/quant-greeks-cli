from binomial import binomial_option_pricing

def test_binomial_call_price():
    price = binomial_option_pricing(S=100, K=100, T=1, r=0.05, sigma=0.2, steps=100, option_type="call", american=False)
    assert abs(price - 10.45) < 0.2

def test_binomial_put_price():
    price = binomial_option_pricing(S=100, K=100, T=1, r=0.05, sigma=0.2, steps=100, option_type="put", american=False)
    assert abs(price - 5.57) < 0.2