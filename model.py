import numpy as np

from scipy.integrate import odeint


PARAMS_ORDER = \
    ['susceptible', 'exposed', 'infected', 'critical', 'recovered', 'deceased']
# source JAMA: 8 days to develop ARDS
di2c = 8.0  # infected to critical
# source CNHC: <70yo - [6-41] med:14 | >=70+yo - [6-19] med:11.5
di2d = 14.0  # infected to dead
dc2d = di2d - di2c
# source https://bit.ly/2KRQWeD
dc2r = 12.0
# source JAMA: median hospital stay - 10 days
di2r = 10.0  # infected to recovered
# source https://bit.ly/3ff307m mean: 5.2
incubation_period = 5.2
# recovery rate(infected->recovered)
gamma = 1.0 / di2r
# rate of infecting(exposed->infected)
sigma = 1.0 / incubation_period


def logistic_r0(t, r0_start, k, x0, r0_end):
    return (r0_start - r0_end) / (1 + np.exp(-k * (-t + x0))) + r0_end


# noinspection PyPep8Naming
def derivatives(y, t, beta, population, pi2c, pc2d):
    """
    beta: expected infection rate per person per day

                         (beta * I * S/N - sigma * E)
                                  |
    -1 * S/N * (beta*I)     sigma * 1 * E     gamma * (1 - pi2c) * I
[S] -----------------> [E]  ------------> [I] ---------------------> [R]
                                          |                        /
                                          |                    /
                                          |                /
                       1/di2c * pi2c * I  |            /
                                          |        / 1/dc2r * (1 - pc2d) * C
                                          |    /
                                         [C] ---------------------> [D]
                                               1/dc2d * pc2d * C
    """
    susceptible, exposed, infected, *_ = y

    dSdt = -beta(t) * infected * susceptible / float(population)
    dEdt = beta(t) * infected * susceptible / float(population) \
        - sigma * exposed
    dIdt = sigma * exposed - 1 / di2c * pi2c * infected \
        - gamma * (1 - pi2c) * infected
    dCdt = 1 / di2c * pi2c * infected - 1 / dc2d * pc2d \
        - (1 - pc2d) * 1 / dc2r
    dRdt = gamma * (1 - pi2c) * infected + (1 - pc2d) * 1 / dc2r
    dDdt = 1 / dc2d * pc2d
    return dSdt, dEdt, dIdt, dCdt, dRdt, dDdt


def model(predict_days, population_, r0_start, k, x0, r0_end, pi2c, pc2d):
    def beta(t_):
        return logistic_r0(t_, r0_start, k, x0, r0_end) * gamma

    # initial vector
    y0 = population_-1, 1, 0, 0, 0, 0

    t = np.linspace(0, predict_days, predict_days, dtype=int)
    ret = odeint(derivatives, y0, t,
                 args=(beta, population_, pi2c, pc2d))
    susceptible, exposed, infected, critical, recovered, deceased = ret.T

    return t, susceptible, exposed, infected, critical, recovered, deceased
