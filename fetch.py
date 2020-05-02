import json
from typing import List

import requests

from base import get_rest_url, TIMELINE, DATA_FIELD, POPULATION_FIELD
from util import get_date_timestamp, get_total, get_new, get_total_deceased


class FetchResult:
    timestamps: List = []
    totals: List = []
    new_cases: List = []
    total_deceased: List = []
    population: int = 0


def retrieve_from_rest(country: str):
    response = requests.get(get_rest_url(country))
    if response.status_code is not requests.codes.ok:
        raise ConnectionError("unable to get json report")

    json_response = json.loads(response.content)
    return json_response[DATA_FIELD]


def retrieve_axises(country: str) -> FetchResult:
    data = retrieve_from_rest(country)
    timeline = data[TIMELINE]

    if not data:
        return FetchResult()
    else:
        fr = FetchResult()
        fr.timestamps = [get_date_timestamp(x) for x in timeline][::-1]
        fr.totals = [get_total(x) for x in timeline][::-1]
        fr.total_deceased = [get_total_deceased(x) for x in timeline][::-1]
        fr.new_cases = [get_new(x) for x in timeline][::-1]
        fr.population = data[POPULATION_FIELD]
        return fr
