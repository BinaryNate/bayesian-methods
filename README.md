# Bayesian Exercises

Exercises and notes from Bayesian Methods for Hackers.

- [Book on GitHub](https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers)
- [Book's Jupyter notebook](https://nbviewer.jupyter.org/github/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/blob/master/Prologue/Prologue.ipynb)
- [PyMC3 on GitHub](https://github.com/pymc-devs/pymc3)

## How the repo was created

```
python3 -m venv env
source env/bin/activate
pip install pymc3
pip install ipython
```

# Notes

## Chapter 1

Summary in my words: Bayesian inference is like a function where:
    - parameters:
        - a prior belief (modeled as a distribution)
        - some new information
    - output: posterior belief (modeled as a distribution)

### Discrete

- Discrete random variable: probability mass function:
    - https://en.wikipedia.org/wiki/Probability_mass_function

- Poisson distribution is for discrete values:
    - https://en.wikipedia.org/wiki/Poisson_distribution

- If a random variable Z has a Poisson mass distribution, we denote this by writing: Z ∼ Poi(λ)

- One useful property of the Poisson distribution is that its expected value is equal to its parameter: `E[Z|λ] = λ`

> λ  is called a parameter of the distribution, and it controls the distribution's shape. For the Poisson distribution, λ can be any positive number. By increasing λ, we add more probability to larger values, and conversely by decreasing λ we add more probability to smaller values. One can describe λ as the intensity of the Poisson distribution.

### Continuous

- Continuous random variable: probability density function:
    - https://en.wikipedia.org/wiki/Probability_density_function

- An example of continuous random variable is a random variable with exponential density.

- When a random variable Z has an exponential distribution with parameter λ, we say Z is exponential and write: Z ∼ Exp(λ)

- Given a specific λ, the expected value of an exponential random variable is equal to the inverse of λ: `E[Z|λ] = 1/λ`

### But what is λ?

> This question is what motivates statistics. In the real world, λ is hidden from us. We see only Z, and must go backwards to try and determine λ.The problem is difficult because there is no one-to-one mapping from Z to λ. Many different methods have been created to solve the problem of estimating λ, but since λ is never actually observed, no one can say for certain which method is best!

> Bayesian inference is concerned with beliefs about what λ might be. Rather than try to guess λ exactly, we can only talk about what λ is likely to be by assigning a probability distribution to λ.

> This might seem odd at first. After all, λ is fixed; it is not (necessarily) random! How can we assign probabilities to values of a non-random variable? Ah, we have fallen for our old, frequentist way of thinking. Recall that under Bayesian philosophy, we can assign probabilities if we interpret them as beliefs. And it is entirely acceptable to have beliefs about the parameter λ.

Summary in my words: Distributions can be used to model the values of a random variable (like a Poisson distribution for discrete values or an exponential distribution for continuous random variables). λ is a parameter that dictates the shape the distribution (higher λ means a higher probability of larger values and vice versa). So, we want to find a likely value for λ to allow us accurately model our data. We can use Bayesian inference to determine the probability for different values of λ.

### Finding λ

- To find λ, we can treat it as a continuous random variable, and thus model it with an exponential distribution.
    - So, if our original model is for a discrete random variable, we'll first have a Poisson distribution for that random variable: C ∼ Poisson(λ)
    - We'll then have a second exponential distribution for finding the λ for the first distribution:  λ ∼ Exp(α)

> A good rule of thumb is to set the exponential parameter (α) equal to the inverse of the average of the count data.

> What about τ? Because of the noisiness of the data, it's difficult to pick out a priori when τ might have occurred. Instead, we can assign a uniform prior belief to every possible day. This is equivalent to saying: τ ∼ DiscreteUniform(1,70) ⇒ P(τ=k) = 1/70

- Discrete uniform distribution: probability distribution wherein a finite number of values are equally likely to be observed; every one of n values has equal probability 1/n.
    - https://en.wikipedia.org/wiki/Discrete_uniform_distribution


### Introducing PyMC3

- B. Cronin has a very motivating description of probabilistic programming:
> Another way of thinking about this: unlike a traditional program, which only runs in the forward directions, a probabilistic program is run in both the forward and backward direction. It runs forward to compute the consequences of the assumptions it contains about the world (i.e., the model space it represents), but it also runs backward from the data to constrain the possible explanations. In practice, many probabilistic programming systems will cleverly interleave these forward and backward operations to efficiently home in on the best explanations.


### Interpretation

> Recall that Bayesian methodology returns a distribution...the wider the distribution, the less certain our posterior belief should be.

> We'll use the posterior samples to answer the following question: what is the expected number of texts at day t, 0 ≤ t ≤70 ? Recall that the expected value of a Poisson variable is equal to its parameter λ. Therefore, the question is equivalent to what is the expected value of λ at time t?

> As explained, the "message count" random variable is Poisson distributed, and therefore lambda (the poisson parameter) is the expected value of "message count".
