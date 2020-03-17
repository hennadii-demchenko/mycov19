import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, num2date
from scipy.optimize import curve_fit

from util import load

data = load('greece')
dates_given = list(data.keys())
values_given = list(data.values())

dates, values = [], []
for date, value in zip(dates_given, values_given):
    if ~np.isnan(value):
        dates.append(date)
        values.append(value)

values = [d for d, _ in sorted(zip(values, dates))]
dates = sorted(dates)
dates_converted = date2num(dates)

x = dates_converted
print(x)
y = np.array([float(i) for i in values])


def func(x, a, b, c):
    return a * np.exp(b * x) + c


xx = np.linspace(1, len(y), num=len(y))
popt, _ = curve_fit(func,  xx,  y, p0=[0.23, .15, -.2])

plt.figure()
plt.scatter(xx, y)
plt.plot(xx, y, 'b+', label="Original Noised Data")
#y1 = np.array([*y, *[func(i, *popt) for i in range(len(x), 2*len(x), 1)]])
xx = np.linspace(0, 2*len(x), num=2*len(x))
plt.plot(xx, func(xx, *popt), 'r-', label="Fitted Curve")
plt.xlim(-2, 1.2*len(x) + 5)
plt.ylim(-55, 2 * np.max(y))
plt.legend()
plt.show()