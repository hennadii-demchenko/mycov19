from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
from scipy.optimize import curve_fit

from util import exp_func, logistic_func, generate_dates_formatter, \
    normalize_dates


# TODO
def get_growth_factor_data(normalized_values):
    ratios = []

    for x in range(len(normalized_values) - 1):
        next_ = normalized_values[x + 1]
        if next_ is np.nan or normalized_values[x] is np.nan \
                or next_ == normalized_values[x]:
            continue
        ratio = next_ / normalized_values[x]
        ratios.append(ratio)
        print(ratio)

    x_, y_ = range(len(ratios)), ratios
    return x_, y_


def add_growth_factor(values):

    x, y = get_growth_factor_data(values)
    z = np.polyfit(x, y, 3)
    p = np.poly1d(z)

    plt.scatter(x, y)
    plt.plot(x, p(x), "r")
    plt.title("Growth factor trend")


def add_predictions(ax, dates, values, predict_days=30):
    dates = normalize_dates(dates)
    x_continue = np.linspace(int(min(dates)),
                             int(max(dates)) + predict_days - 1,
                             num=int(max(dates)) + predict_days)

    popt_exp, _ = curve_fit(exp_func, dates, values)
    popt_log, _ = curve_fit(logistic_func, dates, values, p0=[5, 1, 25])

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


def plot_data(data: Tuple[List, List]):
    x, y = data

    fig = plt.figure(constrained_layout=True)
    fig.set_size_inches(8, 8)
    gs = fig.add_gridspec(nrows=2, ncols=1, figure=fig, hspace=.02)

    ax = fig.add_subplot(gs[0, 0])
    ax.axes.get_xaxis().set_visible(False)
    # add_growth_factor(values) TODO

    ax = fig.add_subplot(gs[1, 0])
    ax.grid(True)
    ax.xaxis.set_major_formatter(FuncFormatter(generate_dates_formatter(x)))
    add_predictions(ax, x, y)

    plt.show()
