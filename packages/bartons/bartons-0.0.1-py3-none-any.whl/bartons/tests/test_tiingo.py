import os
import pytest
from importlib.util import find_spec

pytestmark = pytest.mark.filterwarnings("ignore:pkg_resources:DeprecationWarning:tiingo")


if not find_spec("tiingo"):
    pytest.skip("tiingo library not installed!", allow_module_level=True)

if not os.getenv("TIINGO_API_KEY"):
    pytest.skip("API key not configured!", allow_module_level=True)


@pytest.fixture
def engine():
    from bartons.tiingo import TiingoPrices
    return TiingoPrices()

@pytest.mark.parametrize("freq", ["1min", "5min", "hourly", "daily", "weekly", "monthly"])
@pytest.mark.parametrize("ticker", ["AAPL"])
def test_engine(engine, ticker, freq, max_bars=None):
    result = engine.get_prices(ticker, freq=freq, max_bars=max_bars)
    assert result is not None
    assert len(result) > 0
    if max_bars:
        if freq in ("daily", "weekly", "monthly"):
            assert len(result) <= max_bars
        else:
            assert len(result) == max_bars


