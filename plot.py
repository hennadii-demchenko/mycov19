import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import date2num, num2date
from scipy.optimize import curve_fit


def get_prepared_data(data: dict):
    dates, values = [], []

    for date, value in data.items():
        if ~np.isnan(value):
            dates.append(date)
            values.append(value)

    values = [d for d, _ in sorted(zip(values, dates))]
    dates = sorted(dates)
    dates_converted = date2num(dates)
    return dates_converted, values, dates


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


def add_exponential(values, dates, dates_labels):
    def func(x, a, b, c):
        return a * np.exp(b * x) + c

    totals = np.array(values)
    z4 = np.polyfit(dates, totals, 20)
    p4 = np.poly1d(z4)
    linearized_dates = \
        np.linspace(dates.min(), dates.max() + 5, num=len(dates))
    linearized_dates_labels = num2date(linearized_dates)

    plt.plot(linearized_dates_labels, p4(linearized_dates), '-g')
    plt.scatter(dates_labels, totals)
    plt.plot(dates_labels, totals, '+', color='b')
    plt.title("Exponential (pessimistic) trend")
    plt.xlabel('date')
    plt.ylabel('total cases')


def add_logistic(values, dates):

    def logistic_func(x__, l_, c, k):
        return l_ / (1 + c * np.exp(-k * x__))

    total = np.array(values)
    logistic_offset = dates.max() - dates.min()
    xx = np.linspace(-logistic_offset, logistic_offset, num=len(dates))
    popt, pcov = curve_fit(logistic_func, xx, values, p0=[500, 1, 1])

    plt.plot(xx, logistic_func(xx, *popt), 'r-', label='Fitted function')
    plt.scatter(xx, total)
    plt.title("Logistic function (optimistic) trend")
    plt.xlabel(None)
    plt.xlim(-logistic_offset - 2, logistic_offset + 10)


def plot_data(data: dict):

    fig = plt.figure(constrained_layout=True)
    fig.set_size_inches(8, 8)
    gs = fig.add_gridspec(nrows=3, ncols=1, figure=fig, hspace=.02)

    dates, values, dates_labels = get_prepared_data(data)

    ax = fig.add_subplot(gs[0, 0])
    ax.axes.get_xaxis().set_visible(False)
    add_growth_factor(values)

    ax = fig.add_subplot(gs[1, 0])
    ax.tick_params(axis='x', labelrotation=90, labelsize=7, pad=.1)
    add_exponential(values, dates, dates_labels)

    ax = fig.add_subplot(gs[2, 0])
    ax.axes.get_xaxis().set_visible(False)
    add_logistic(values, dates)

    plt.show()
