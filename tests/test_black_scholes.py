import pytest
from black_scholes import black_scholes_price

def test_invalid_option_type():
    with pytest.raises(ValueError):
        black_scholes_price("invalid", 100, 100, 1, 0.05, 0.2)