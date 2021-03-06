# The code from the example in 1.4 with some tweaks:
# - had to change `normed=True` to `density=True`
# - added plt.show() at the end
# - Added print statements for the exercises in 1.7
import numpy as np
import pymc3 as pm
import theano.tensor as tt
from matplotlib import pyplot as plt
from IPython.core.pylabtools import figsize

count_data = np.loadtxt("data/txtdata.csv")
n_count_data = len(count_data)

with pm.Model() as model:
    alpha = 1.0/count_data.mean()
    lambda_1 = pm.Exponential("lambda_1", alpha)
    lambda_2 = pm.Exponential("lambda_2", alpha)

    tau = pm.DiscreteUniform("tau", lower=0, upper=n_count_data - 1)

    idx = np.arange(n_count_data)
    lambda_ = pm.math.switch(tau > idx, lambda_1, lambda_2)
    observation = pm.Poisson("obs", lambda_, observed=count_data)

    step = pm.Metropolis()
    trace = pm.sample(10000, tune=5000, step=step)

    lambda_1_samples = trace['lambda_1']
    lambda_2_samples = trace['lambda_2']
    tau_samples = trace['tau']

    figsize(12.5, 10)
    #histogram of the samples:

    ax = plt.subplot(311)
    ax.set_autoscaley_on(False)

    plt.hist(lambda_1_samples, histtype='stepfilled', bins=30, alpha=0.85,
            label="posterior of $\lambda_1$", color="#A60628", density=True)
    plt.legend(loc="upper left")
    plt.title(r"""Posterior distributions of the variables
        $\lambda_1,\;\lambda_2,\;\tau$""")
    plt.xlim([15, 30])
    plt.xlabel("$\lambda_1$ value")

    ax = plt.subplot(312)
    ax.set_autoscaley_on(False)
    plt.hist(lambda_2_samples, histtype='stepfilled', bins=30, alpha=0.85,
            label="posterior of $\lambda_2$", color="#7A68A6", density=True)
    plt.legend(loc="upper left")
    plt.xlim([15, 30])
    plt.xlabel("$\lambda_2$ value")

    plt.subplot(313)
    w = 1.0 / tau_samples.shape[0] * np.ones_like(tau_samples)
    plt.hist(tau_samples, bins=n_count_data, alpha=1,
            label=r"posterior of $\tau$",
            color="#467821", weights=w, rwidth=2.)
    plt.xticks(np.arange(n_count_data))

    plt.legend(loc="upper left")
    plt.ylim([0, .75])
    plt.xlim([35, len(count_data)-20])
    plt.xlabel(r"$\tau$ (in days)")
    plt.ylabel("probability")

    # Exercise 1.7.1
    print(f'lambda_1_samples mean: {lambda_1_samples.mean()}')
    print(f'lambda_2_samples mean: {lambda_2_samples.mean()}')

    # Exercise 1.7.2
    relative_increase_samples = (lambda_2_samples - lambda_1_samples) / lambda_1_samples
    expected_percentage_increase = relative_increase_samples.mean()
    print(f'expected percentage increase in text-message rates: {expected_percentage_increase}')

    # Exercise 1.7.3
    ix = tau_samples < 45
    print(f'λ1 given that τ is less than 45: {lambda_1_samples[ix].mean()}')

    plt.show()
