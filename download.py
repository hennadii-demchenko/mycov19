import os
from urllib import parse

import requests
from bs4 import BeautifulSoup

from base import REPORTS_DIR, REPORTS_PAGE_URL


def _download_report(url):
    file_name = url.path.split('/')[-1].split('?')[0]
    file_path = REPORTS_DIR / file_name
    verdict = '[%s] '
    if not os.path.exists(file_path):
        response = requests.get(url.geturl())
        if response.status_code is requests.codes.ok:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            out = verdict % 'DOWNLOAD SUCCESS'
        else:
            out = verdict % 'DOWNLOAD FAILURE'
    else:
        out = verdict % 'DOWNLOAD SKIP'
    print(out + file_name)


def download_reports():
    response = requests.get(REPORTS_PAGE_URL)
    if response.status_code is not requests.codes.ok:
        raise ConnectionError("unable to get reports page")

    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.select('div.sf-content-block div p a')
    url = parse.urlsplit(REPORTS_PAGE_URL)

    # noinspection PyProtectedMember
    [_download_report(url._replace(path=l.get('href')))
     for l in links if l.text]
