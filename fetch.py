import json
import requests

from base import get_rest_url, FEATURES
from util import get_date_timestamp, get_total, get_new


def retrieve_from_rest(country: str):
    response = requests.get(get_rest_url(country))
    if response.status_code is not requests.codes.ok:
        raise ConnectionError("unable to get json report")

    json_response = json.loads(response.content)
    return json_response[FEATURES]


def retrieve_axises(country: str):
    data = retrieve_from_rest(country)
    if not data:
        return [], []
    else:
        return zip(*[(get_date_timestamp(x), get_total(x), get_new(x))
                     for x in data])
