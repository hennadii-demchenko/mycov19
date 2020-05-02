import numpy as np
import lmfit
from lmfit import Parameters
from scipy.optimize import curve_fit


def fit_model_to_data(data, population, fit_index):
    fit_params = Parameters()
    fit_params.add('r0_start',
                   3.6, min=2.0, max=5.0, vary=True)
    fit_params.add('k',
                   4.0, min=.01, max=5.0, vary=True)
    fit_params.add('x0',
                   10., min=0.0, max=200, vary=True)
    fit_params.add('r0_end',
                   0.6, min=0.3, max=3.5, vary=True)
    fit_params.add('pi2c',
                   .04, min=.01, max=0.3, vary=True)
    fit_params.add('pc2d',
                   0.3, min=0.1, max=0.9, vary=True)

    initial_guesses = [p.value for f, p in fit_params.items()]
    bounds = list(zip(*[(p.min, p.max) for f, p in fit_params.items()]))

    def fitter(x, r0_start, k, x0, r0_end, pi2c, pc2d):
        from model import model
        ret = model(len(data), population,
                    r0_start, k, x0, r0_end, pi2c, pc2d)
        return ret[fit_index][x]

    xdata = np.linspace(0, len(data), len(data), dtype=int)

    popt_model, pcov_model = curve_fit(
        fitter, xdata, data, p0=initial_guesses, bounds=bounds, maxfev=100_000)

    model2fit = lmfit.Model(fitter)
    x_data = np.linspace(0, len(data) - 1, len(data), dtype=int)
    return model2fit.fit(data, fit_params, x=x_data)
