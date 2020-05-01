import json
import requests

from base import get_rest_url, TIMELINE, DATA_FIELD
from util import get_date_timestamp, get_total, get_new


def retrieve_from_rest(country: str):
    response = requests.get(get_rest_url(country))
    if response.status_code is not requests.codes.ok:
        raise ConnectionError("unable to get json report")

    json_response = json.loads(response.content)
    return json_response[DATA_FIELD][TIMELINE]


def retrieve_axises(country: str):
    data = retrieve_from_rest(country)
    ts, totals, new = [], [], []

    if not data:
        return [], [], []

    for x in data:
        ts.append(get_date_timestamp(x))
        totals.append(get_total(x))
        new.append(get_new(x))
    # reversed new -> old for this API
    return ts[::-1], totals[::-1], new[::-1]
