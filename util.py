from datetime import datetime, timedelta

from base import DATA_TIMESTAMP, ATTRIBUTES, TOTAL_CASES, NEW_CASES
import numpy as np


def get_date_timestamp(sample_):
    return sample_[ATTRIBUTES][DATA_TIMESTAMP]


def get_total(sample_):
    return sample_[ATTRIBUTES][TOTAL_CASES]


def get_new(sample_):
    return sample_[ATTRIBUTES][NEW_CASES]


def exp_func(x, a, b, c):
    return a * np.exp(b * x) + c


def logistic_func(x__, l_, c, k):
    return l_ / (1 + c * np.exp(-k * x__))


def generate_dates_formatter(dates):
    # noinspection PyUnusedLocal
    def formatter(tick_val, *args):
        return datetime.strftime(datetime.fromtimestamp(min(dates) / 1000) +
                                 timedelta(days=int(tick_val)), '%Y-%m-%d')
    return formatter


def normalize_dates(dates):
    dates = [datetime.fromtimestamp(ts / 1000) for ts in dates]

    return np.array([0, *np.cumsum(
        np.diff(dates).astype('timedelta64[D]') / np.timedelta64(1, 'D'))])