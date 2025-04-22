import os
import pytest
from importlib.util import find_spec


pytestmark = pytest.mark.filterwarnings("ignore:websockets:DeprecationWarning:")


if not find_spec("polygon"):
    pytest.skip("Polygon library not installed!", allow_module_level=True)


if not os.getenv("POLYGON_API_KEY"):
    pytest.skip("API key not configured!", allow_module_level=True)


PARAMS = [
    ["1min", None],
    ["1min", 5000],
    ["1min", 10000],
    ["1min", 50000],
    ["5min", None],
    ["5min", 5000],
    ["15min", None],
    ["15min", 5000],
    ["30min", None],
    ["30min", 5000],
    ["hourly", None],
    ["hourly", 5000],
    ["daily", None],
    ["daily", 5000],
    ["weekly", None],
    ["weekly", 5000],
    ["monthly", None],
    ["monthly", 5000],
]


@pytest.fixture
def engine():
    from bartons.polygon import polygon_engine
    return polygon_engine()


@pytest.mark.parametrize("ticker", ["AAPL"])
@pytest.mark.parametrize("freq,max_bars", PARAMS)
def test_engine(engine, ticker, freq, max_bars):
    result = engine.get_prices(ticker, freq=freq, max_bars=max_bars)
    assert result is not None
    assert len(result) > 0
    if max_bars:
        if freq in ("daily", "weekly", "monthly"):
            assert len(result) <= max_bars
        else:
            assert len(result) == max_bars

