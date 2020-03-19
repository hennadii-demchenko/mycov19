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


def annotate_values(values, dates, floats=False):
    ys = [50, 10, 30]
    for i, text in enumerate(values[1:]):
        template = '%.1f' if floats else '%s'
        plt.annotate(template % values[i], (dates[i], values[i]), ha='center',
                     textcoords="offset points", xytext=(-5, ys[i % 3]),
                     arrowprops=dict(arrowstyle='-|>', lw=.3, ls='--'))


def logistic_func(x, a, b, c, d):
    return a / (1. + np.exp(-c * (x-d))) + b


def exp_func(x, a, b, c, d):
    return a * np.exp(b * (x-d)) + c


def get_ratios_sequence(values_):
    data = np.array(values_)
    data = data[data > 0]
    ratios = np.divide(data[1:], data[:-1])
    ratios[np.isnan(ratios)] = 0
    ratios[np.abs(ratios) == np.inf] = 0
    return ratios


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