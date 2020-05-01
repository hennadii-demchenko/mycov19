from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter, FixedLocator
from scipy.optimize import curve_fit

from util import exp_func, generate_dates_formatter, \
    normalize_dates, get_ratios_sequence, logistic_func, annotate_values

PREDICT_DAYS = 14


def setup_plot(ax, timestamps, locate_dates, predict_days=PREDICT_DAYS):
    dates = normalize_dates(timestamps)
    plt.grid(True, which='both')
    ax.xaxis.set_major_formatter(
        FuncFormatter(generate_dates_formatter(timestamps)))
    ax.xaxis.set_minor_locator(FixedLocator(locate_dates))
    plt.xlim(min(dates) - 1, max(dates) + 0.8 * predict_days)


def plot_raw(ax, timestamps, values):
    dates = normalize_dates(timestamps)
    setup_plot(ax, timestamps, dates)
    plt.scatter(dates, values)
    plt.plot(values)
    annotate_values(values, dates)


def add_growth_factor(ax, timestamps, values, predict_days=PREDICT_DAYS):
    dates = normalize_dates(timestamps)
    setup_plot(ax, timestamps, dates)

    non_zero_values = np.array(values)
    non_zero_dates = np.array(dates)[non_zero_values > 0]
    non_zero_values = non_zero_values[non_zero_values > 0]
    ratios = [0, *get_ratios_sequence(non_zero_values)]
    annotate_values(ratios, non_zero_dates, floats=True)
    plt.ylim(-.1, max(ratios) + 3)

    plt.plot(non_zero_dates, ratios, "bo", label="Growth ratios")
    plt.plot(non_zero_dates, ratios, "b")
    plt.plot(non_zero_dates, np.ones(len(non_zero_dates)), 'r',
             label="1.0 Threshold", alpha=0.6)
    plt.legend()


def add_predictions(ax, timestamps, values, predict_days=PREDICT_DAYS):
    dates = normalize_dates(timestamps)
    x_continue = np.linspace(int(min(dates)),
                             int(max(dates)) + predict_days - 1,
                             num=int(max(dates)) + predict_days)
    setup_plot(ax, timestamps, x_continue)
    plt.ylim(-33, 6.6 * np.max(values))

    popt_exp, _ = curve_fit(exp_func, dates, values,
                            p0=[1, 1, 1, -1], maxfev=100_000)
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


def plot_data(country, data: Tuple[List, List, List]):
    x, totals, new_cases = data

    fig = plt.figure(constrained_layout=True)
    fig.suptitle(f"{country} analytics",
                 fontsize=12, x=0.9, y=.995)
    fig.set_size_inches(10, 6)
    gs = fig.add_gridspec(nrows=2, ncols=1, figure=fig, hspace=.02)

    ax = fig.add_subplot(gs[0, 0])
    plt.title("Growth ratio")
    add_growth_factor(ax, x, new_cases)

    ax = fig.add_subplot(gs[1, 0])
    plt.title("Total cases cumulative")
    # noinspection PyBroadException
    try:
        add_predictions(ax, x, totals)
    except Exception:
        plot_raw(ax, x, totals)

    plt.show()
