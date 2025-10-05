import pytest
from implied_vol import implied_volatility

def test_implied_volatility_no_convergence():
    # This should fail to converge because price is impossible for these params
    with pytest.raises(RuntimeError, match="Failed to converge"):
        implied_volatility("call", 100, 100, 1, 0.05, 200)