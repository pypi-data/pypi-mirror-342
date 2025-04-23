from src.analystock_api.query_generic import _make_request


def get_instruments(api_key):
    """Get a list of all instruments and their characteristics. Optional filters supported."""
    return _make_request("instruments/", api_key)


def get_sectors(api_key):
    """Get a list of all available sectors."""
    return _make_request("sectors/", api_key)


def get_subindustries(api_key):
    """Get a list of all sub-industries."""
    return _make_request("subindustries/", api_key)


def get_currencies(api_key):
    """Get a list of all supported currencies."""
    return _make_request("currencies/", api_key)


def get_countries(api_key):
    """Get a list of all available countries."""
    return _make_request("countries/", api_key)


def get_exchanges(api_key):
    """Get a list of all stock exchanges."""
    return _make_request("exchanges/", api_key)


def get_foreign_exchanges(api_key):
    """Get a list of all foreign exchange rate pairs."""
    return _make_request("foreign_exchanges/", api_key)
