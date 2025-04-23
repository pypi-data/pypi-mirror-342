from src.analystock_api.query_generic import _make_request


def get_instruments_ratios(api_key, tickers=None):
    """Retrieve valuation ratios like P/E, EV/EBITDA, etc."""
    params = {'tickers': ','.join(tickers)} if tickers else None
    return _make_request("instruments_ratios/", api_key, params)


def get_instruments_key_metrics(api_key, tickers=None):
    """Get core financial metrics like revenue, EBITDA."""
    params = {'tickers': ','.join(tickers)} if tickers else None
    return _make_request("instruments_key_metrics/", api_key, params)


def get_instruments_growth(api_key, tickers=None):
    """Return growth metrics like revenue growth, earnings growth."""
    params = {'tickers': ','.join(tickers)} if tickers else None
    return _make_request("instruments_growth/", api_key, params)


def get_instruments_balance_sheet(api_key, tickers=None):
    """Get detailed balance sheet data."""
    params = {'tickers': ','.join(tickers)} if tickers else None
    return _make_request("instruments_balance_sheet/", api_key, params)


def get_instruments_income_statement(api_key, tickers=None):
    """Get income statement for a company."""
    params = {'tickers': ','.join(tickers)} if tickers else None
    return _make_request("instruments_income_statement/", api_key, params)


def get_instruments_cf_statement(api_key, tickers=None):
    """Get cash flow statement data."""
    params = {'tickers': ','.join(tickers)} if tickers else None
    return _make_request("instruments_cf_statement/", api_key, params)


def get_instruments_hlights(api_key, tickers=None):
    """Summary highlights for a company."""
    params = {'tickers': ','.join(tickers)} if tickers else None
    return _make_request("instruments_hlights/", api_key, params)


def get_instruments_sector_hlights(api_key, sector_id=None):
    """Get sector average highlights."""
    params = {'sector': sector_id} if sector_id else None
    return _make_request("instruments_sector_hlights/", api_key, params)


def get_instruments_all_hlights(api_key):
    """Get all highlights for all instruments and sectors."""
    return _make_request("instruments_all_hlights/", api_key)
