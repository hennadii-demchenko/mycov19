from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter, FixedLocator
from scipy.optimize import curve_fit

from util import exp_func, generate_dates_formatter, \
    normalize_dates, get_ratios_sequence, logistic_func, annotate_values


def plot_raw(ax, timestamps, values):
    plt.grid(True, which='both')
    dates = normalize_dates(timestamps)

    ax.xaxis.set_major_formatter(
        FuncFormatter(generate_dates_formatter(timestamps)))
    ax.xaxis.set_minor_locator(FixedLocator(dates))

    plt.scatter(dates, values)
    plt.plot(values)
    annotate_values(values, dates)


def add_growth_factor(ax, values):
    diffs = np.diff(sorted(set(values)))
    ratios = get_ratios_sequence(diffs[diffs > 0])

    plt.plot(ratios, label="Growth ratio")
    plt.plot(ratios, "b+")
    plt.plot(np.ones(len(ratios)), 'r', label="1.0 Threshold")
    plt.legend()


def add_predictions(ax, timestamps, values, predict_days=14):
    dates = normalize_dates(timestamps)
    x_continue = np.linspace(int(min(dates)),
                             int(max(dates)) + predict_days - 1,
                             num=int(max(dates)) + predict_days)

    ax.xaxis.set_major_formatter(
        FuncFormatter(generate_dates_formatter(timestamps)))
    ax.xaxis.set_minor_locator(FixedLocator(x_continue))
    plt.xlim(-2, max(dates) + 0.8 * predict_days)
    plt.ylim(-33, 6.6 * np.max(values))

    popt_exp, _ = curve_fit(exp_func, dates, values, maxfev=100_000)
    popt_log, _ = curve_fit(logistic_func, dates, values,
                            p0=[1e7, 10, .25, 55], maxfev=100_000)
    [print(p) for p in [popt_exp, popt_log]]

    y_exp, y_log = [f(x_continue, *opt) for f, opt in
                    zip([exp_func, logistic_func],
                        [popt_exp, popt_log])]

    plt.scatter(dates, values)
    annotate_values(values, dates)

    plt.plot(dates, values, 'b+', label="Recorded data")
    plt.plot(x_continue, y_exp, 'r-', label="Predicted Exponential outcome")
    plt.plot(x_continue, y_log, 'g--', label="Predicted Logistics outcome")
    plt.legend()
и

def plot_data(country, data: Tuple[List, List]):
    x, y = data

    fig = plt.figure(constrained_layout=True)
    fig.suptitle(f"{country.capitalize()} analytics",
                 fontsize=12, x=0.9, y=.995)
    fig.set_size_inches(10, 6)
    gs = fig.add_gridspec(nrows=2, ncols=1, figure=fig, hspace=.02)

    ax = fig.add_subplot(gs[0, 0])
    plt.title("Growth ratio")
    ax.grid(True)
    ax.axes.get_xaxis().set_visible(False)
    add_growth_factor(ax, y)

    ax = fig.add_subplot(gs[1, 0])
    plt.title("Total cases cumulative")
    ax.grid(True, which='both')
    # noinspection PyBroadException
    try:
        add_predictions(ax, x, y)
    except Exception:
        plot_raw(ax, x, y)

    plt.show()
