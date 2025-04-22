import pytest
from importlib.util import find_spec


if not find_spec("yfinance"):
    pytest.skip("yfinance library not installed!", allow_module_level=True)


@pytest.fixture
def engine():
    from bartons.yahoo import YahooPrices
    return YahooPrices()


@pytest.mark.parametrize("ticker", ["AAPL"])
@pytest.mark.parametrize("freq", ["daily", "weekly", "monthly"])
@pytest.mark.parametrize("max_bars", [None, 5000])
def test_engine(engine, ticker, freq, max_bars):
    result = engine.get_prices(ticker, freq=freq, max_bars=max_bars)
    assert result is not None
    assert len(result) > 0
    if max_bars:
        if freq in ("daily", "weekly", "monthly"):
            assert len(result) <= max_bars
        else:
            assert len(result) == max_bars

