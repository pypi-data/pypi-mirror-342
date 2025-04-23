from src.analystock_api.query_generic import _make_request


def get_earnings(api_key, ticker=None):
    """Retrieve upcoming and past earnings announcements for a specific stock."""
    params = {'ticker': ticker} if ticker else None
    return _make_request("earnings/", api_key, params)

def get_historical_comments(api_key, tickers=None):
    """Get past commentary for the specified stock tickers."""
    params = {'tickers': ','.join(tickers)} if tickers else None
    return _make_request("histo_stock_comment/", api_key, params)

def get_market_update(api_key):
    """Get a general market update and commentary."""
    return _make_request("market_update/", api_key)

def get_stock_sentiment(api_key, ticker=None):
    """Get the sentiment score for a specific stock."""
    params = {'ticker': ticker} if ticker else None
    return _make_request("stock_sentiment/", api_key, params)