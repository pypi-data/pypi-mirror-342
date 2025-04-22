from pytest import mark

from bartons.prices import get_prices

SOURCE = "random"


@mark.parametrize("max_bars", [None, 500, 5000])
@mark.parametrize("freq", ["minute", "daily", "weekly", "monthly"])
@mark.parametrize("ticker", ["AAA"])
def test_prices(ticker, freq, max_bars):
    result = get_prices(ticker, freq=freq, max_bars=max_bars, source=SOURCE)
    assert result is not None
    assert len(result) > 0
