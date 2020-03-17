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
    if not len(data):
        return [], []

    data, dates, total_cases = iter(data), [], []

    while True:
        try:
            sample = next(data)
            dates.append(get_date_timestamp(sample))
            total_cases.append(get_total(sample))
        except StopIteration:
            # noinspection PyUnboundLocalVariable
            total_cases[-1] = total_cases[-1] + get_new(sample)
            break
    return dates, total_cases
