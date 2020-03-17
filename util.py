import io
import os
import pickle

import requests
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

from base import REPORTS_DIR, STORED_DIR


def date_from_report(report):
    from datetime import datetime
    return datetime.strptime(report.name.split('-')[0], '%Y%m%d')


def get_report_text(report):
    resource_manager = PDFResourceManager()
    with io.StringIO() as f:
        converter = TextConverter(resource_manager, f)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)

        with open(report.absolute(), 'rb') as fh:
            for p in PDFPage.get_pages(
                    fh, caching=True, check_extractable=True):
                page_interpreter.process_page(p)
            text = f.getvalue()

        converter.close()

    return text if text else [""]


def load(country: str) -> dict:
    stored = STORED_DIR / country
    return pickle.load(open(stored.absolute(), 'rb')) \
        if os.path.exists(stored) else {}


def dump(country: str, new_data: dict):
    stored = STORED_DIR / country
    pickle.dump(new_data, open(stored, 'wb'))
