from src.analystock_api.query_generic import _make_request

def get_screener_view(api_key):
    """Get filtered view of instruments based on internal screener logic."""
    return _make_request("screener_view/", api_key)

def get_last_a_score_all(api_key):
    """Retrieve the latest A-Score for all instruments."""
    return _make_request("last_a_score_all/", api_key)

def get_histo_a_score(api_key, tickers=None):
    """Retrieve historical A-Score data for specified tickers."""
    params = {'tickers': ','.join(tickers)} if tickers else None
    return _make_request("histo_a_score/", api_key, params)

def get_last_sector_a_score(api_key, sector_id=None):
    """Retrieve latest A-Score per sector."""
    params = {'sector_id': sector_id} if sector_id else None
    return _make_request("last_secto_a_score/", api_key, params)

def get_country_a_score(api_key, country_code=None):
    """Return A-Score averaged by country."""
    params = {'country_code': country_code} if country_code else None
    return _make_request("country_a_score/", api_key, params)