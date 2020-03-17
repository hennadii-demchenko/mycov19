import numpy as np

from base import REPORTS_DIR
from util import get_report_text, date_from_report, load, dump


def _parse_report(report, country):
    import re
    text = get_report_text(report)
    lines = text.splitlines()

    table2_anchor = None
    for lineno, line in enumerate(lines):
        if 'table 2' in line.lower():
            table2_anchor = lineno

    if table2_anchor is None:
        print(f'unable to locate countries table for {report.name}')

    re_country = re.compile(country + r'\s+([^A-Za-z]+)', re.IGNORECASE)
    data_re = re.search(re_country, "".join(lines[table2_anchor:]))
    if data_re is None:
        print(f"unable to retrieve {country} data")
        return np.nan
    data_raw = data_re.group(1)
    data_raw = data_raw.replace('(', '').replace(')', '')

    try:
        return int(data_raw.split()[0])
    except (TypeError, ValueError):
        return np.nan


def parse_reports(country: str):
    print()
    print(f"Getting reports from {country.capitalize()}")
    stored_data = load(country)
    cache_ = "[CACHE %s]"

    for report in REPORTS_DIR.glob('*.pdf'):
        report_date = date_from_report(report)
        with_date = f"[{report_date.date()}] %s"

        print(with_date % report.name)
        if report_date not in stored_data:
            cache_status = cache_ % "MISS"
            total_cases = _parse_report(report, country)
            stored_data[report_date] = total_cases
        else:
            cache_status = cache_ % " HIT"
            total_cases = stored_data[report_date]

        print(with_date % cache_status
              + f" {total_cases} total case(s) was(were) reported")
        print()

    dump(country, stored_data)
    print()
