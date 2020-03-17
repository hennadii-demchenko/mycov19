from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter, MultipleLocator, FixedLocator
from scipy.optimize import curve_fit

from util import exp_func, logistic_func, generate_dates_formatter, \
    normalize_dates, get_ratios_sequence


def plot_raw(ax, timestamps, values):
    plt.grid(True, which='both')
    dates = normalize_dates(timestamps)

    ax.xaxis.set_major_formatter(
        FuncFormatter(generate_dates_formatter(timestamps)))
    ax.xaxis.set_minor_locator(FixedLocator(dates))

    plt.scatter(dates, values)
    plt.plot(values)
    for i, text in enumerate(values):
        if i > 0 and values[i] > values[i - 1]:
            plt.annotate(values[i], (dates[i], values[i]), ha='center',
                         textcoords="offset points", xytext=(-20, 20),
                         arrowprops=dict(arrowstyle='simple', lw=.3, ls='--'))


def add_growth_factor(ax, values):
    diffs = np.diff(sorted(set(values)))
    ratios = get_ratios_sequence(diffs[diffs > 0])

    plt.plot(ratios, label="Growth ratio")
    plt.plot(ratios, "b+")
    plt.plot(np.ones(len(ratios)), 'r', label="1.0 Threshold")
    plt.legend()


def add_predictions(ax, timestamps, values, predict_days=14):
    dates = normalize_dates(timestamps)

    ax.xaxis.set_major_formatter(
        FuncFormatter(generate_dates_formatter(timestamps)))
    x_continue = np.linspace(int(min(dates)),
                             int(max(dates)) + predict_days - 1,
                             num=int(max(dates)) + predict_days)
    ax.xaxis.set_minor_locator(FixedLocator(x_continue))

    popt_exp, _ = curve_fit(exp_func, dates, values)
    popt_log, _ = curve_fit(logistic_func, dates, values, p0=[5, 1, 25],
                            bounds=[1e-2, 1e10])

    plt.xlim(-2, max(dates) + 0.8 * predict_days)
    plt.ylim(-33, 6.6 * np.max(values))

    plt.scatter(dates, values)
    for i, text in enumerate(values):
        if i > 0 and values[i] > values[i - 1]:
            plt.annotate(values[i], (dates[i], values[i]), ha='center',
                         textcoords="offset points", xytext=(-20, 20),
                         arrowprops=dict(arrowstyle='simple', lw=.3, ls='--'))

    plt.plot(dates, values, 'b+', label="Recorded data")
    plt.plot(x_continue, exp_func(x_continue, *popt_exp), 'r-',
             label="Predicted Exponential outcome")
    plt.plot(x_continue, logistic_func(x_continue, *popt_log), 'g-',
             label="Predicted Logistics outcome")
    plt.legend()


def plot_data(data: Tuple[List, List]):
    x, y = data

    fig = plt.figure(constrained_layout=True)
    fig.set_size_inches(10, 6)
    gs = fig.add_gridspec(nrows=2, ncols=1, figure=fig, hspace=.02)

    ax = fig.add_subplot(gs[0, 0])
    plt.title("Growth ratio")
    ax.grid(True)
    add_growth_factor(ax, y)

    ax = fig.add_subplot(gs[1, 0])
    plt.title("Total cases cumulative")
    ax.grid(True, which='both')
    # noinspection PyBroadException
    try:
        add_predictions(ax, x, y)
    except Exception:
        ax = fig.add_subplot(gs[1, 0])
        plot_raw(ax, x, y)

    plt.show()
