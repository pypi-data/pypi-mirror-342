import requests

BASE_URL = "https://www.analystock.ai/api/api_query/"


def _make_request(endpoint, api_key, extra_params=None):
    url = f"{BASE_URL}{endpoint}"
    params = {'api_key': api_key}

    if extra_params:
        params.update(extra_params)

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Request to {url} failed: {response.status_code} - {response.text}")