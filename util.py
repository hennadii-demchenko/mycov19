from datetime import datetime, timedelta

from base import DATA_TIMESTAMP, ATTRIBUTES, TOTAL_CASES, NEW_CASES
import numpy as np
import matplotlib.pyplot as plt


def get_date_timestamp(sample_):
    return sample_[ATTRIBUTES][DATA_TIMESTAMP]


def get_total(sample_):
    return sample_[ATTRIBUTES][TOTAL_CASES]


def get_new(sample_):
    return sample_[ATTRIBUTES][NEW_CASES]


def annotate_values(values, dates):
    for i, text in enumerate(values):
        if i > 0 and values[i] > values[i - 1]:
            plt.annotate(values[i], (dates[i], values[i]), ha='center',
                         textcoords="offset points", xytext=(-20, 20),
                         arrowprops=dict(arrowstyle='simple', lw=.3, ls='--'))


def logistic_func(x, a, b, c, d):
    return a / (1. + np.exp(-c * (x-d))) + b


def exp_func(x, a, b, c, d):
    return a * np.exp(b * (x-d)) + c


def get_ratios_sequence(values_):
    return np.divide(values_[1:], values_[:-1])


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