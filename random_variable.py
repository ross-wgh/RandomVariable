import numpy as np

# Does not have generalized X^2 behavior because X^2 (the second moment) is different for each type of random variable
# and is not scalable. X^3 is computed quite differently from X^2.

# Also, the sum of two i.i.d. random variables generally doesn't follow the same distribution that they did originally,
# although this is the case for the sum of i.i.d. normal variables.

class RandomVariable:

    # Every random variable has a mean and variance
    def __init__(self, mean, variance):
        self.mean = mean
        self.variance = variance

    def __add__(self, other):
        if type(other) in [int, float]:
            return RandomVariable(self.mean + other, self.variance)
        # General form of random variable. eg: Adding a Normal RV to a Gamma RV
        elif issubclass(self.__class__, RandomVariable) and issubclass(other.__class__, RandomVariable):
            return RandomVariable(self.mean + other.mean, self.variance + other.variance)
        else:
            raise TypeError(f"You cannot add a {other.__class__.__name__} to a Random Variable")

    def __radd__(self, other):
        return self.__add__(other)

    def add_cov(self, other, covariance=0, corr=0):
        if type(self) == type(other):
            if covariance == 0 and corr == 0:
                return self.__add__(other)
            # Input of covariance takes precedence over correlation, although they effectively do the same thing since
            # we know the variances of both random variables being added
            elif covariance != 0:
                return RandomVariable(self.mean + other.mean, self.variance + other.variance + 4 * covariance)
            elif corr != 0:
                return RandomVariable(self.mean + other.mean, self.variance + other.variance + 2 * corr *
                                      (self.variance**.5 * other.variance**.5))
        else:
            raise TypeError(f"You cannot add a {other.__class__.__name__} to a Random Variable")

    def __sub__(self, other):
        if type(other) in [int, float]:
            return RandomVariable(self.mean - other, self.variance)
        elif issubclass(self.__class__, RandomVariable) and issubclass(other.__class__, RandomVariable):
            return RandomVariable(self.mean - other.mean, self.variance + other.variance)
        else:
            raise TypeError(f"You cannot subtract a {other.__class__.__name__} from a Random Variable")

    def sub_cov(self, other, covariance=0, corr=0):
        if covariance == 0 and corr == 0:
            return self.__sub__(other)
        # Input of covariance takes precedence over correlation, although they effectively do the same thing since we
        # know the variances of both random variables being added
        elif covariance != 0:
            return RandomVariable(self.mean - other.mean, self.variance + other.variance - 4 * covariance)
        elif corr != 0:
            return RandomVariable(self.mean - other.mean, self.variance + other.variance - 2 * corr *
                                  (self.variance**.5 * other.variance**.5))

    def __mul__(self, other):
        # In general a random variable does not always follow the same distribution as when it is
        # multiplied by a constant. eg: Beta distribution
        if type(other) in [int, float]:
            # When normal, this returns self.var * other ** 2 for the sigma parameter, making incorrect calculation.
            return RandomVariable(self.mean * other, self.variance * other ** 2)
        elif issubclass(self.__class__, RandomVariable) and issubclass(other.__class__, RandomVariable):
            return RandomVariable(self.mean * other.mean, (self.variance + self.mean ** 2) *
                                  (other.variance + other.mean ** 2) - self.mean ** 2 * other.mean ** 2)
        else:
            raise TypeError(f"You cannot multiply a {other.__class__.__name__} to a Random Variable")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        # Division of two random variables is not currently supported, but dividing by a constant is.
        if type(other) in (int, float):
            return RandomVariable(self.mean * other, self.variance * (1/other) ** 2)
        else:
            raise TypeError(f"You cannot divide a Random Variable by a {other.__class__.__name__}")

    def __str__(self):
        if type(self).__name__ != 'RandomVariable':
            return f"This is a {type(self).__name__} random variable with mean: {self.mean} and variance: {self.variance}"
        else:
            return f"This is a random variable with mean: {self.mean} and variance: {self.variance}"


class Normal(RandomVariable):
    def __init__(self, mean=0, sd=1):
        self.mean = mean
        self.sd = sd
        self.variance = sd ** 2

    def __add__(self, other):
        if type(other) in [int, float]:
            return Normal(self.mean + other, self.sd)
        elif type(self) == type(other):
            return Normal(self.mean + other.mean, (self.sd**2 + other.sd**2)**.5)
        else:
            return RandomVariable.__add__(self, other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if type(other) in [int, float]:
            return Normal(self.mean - other, self.sd)
        elif type(self) == type(other):
            return Normal(self.mean - other.mean, self.sd + other.sd)
        else:
            return RandomVariable.__sub__(self, other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if type(other) in [int, float]:
            return Normal(self.mean * other, self.sd * other)
        elif self == other and self.mean == 0 and self.sd == 1:
            return ChiSquare(1)
        else:
            return RandomVariable.__mul__(self, other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def generate(self, sample_size):
        return np.random.normal(self.mean, self.sd, sample_size)


class ChiSquare(Normal):
    def __init__(self, df):
        self.df = df
        self.mean = df
        self.variance = 2 * df

    def __add__(self, other):
        if type(other) == type(self):
            return ChiSquare(self.df + other.df)
        else:
            return RandomVariable.__add__(self, other)

    def generate(self, sample_size):
        return np.random.chisquare(self.df, sample_size)


class Binomial(RandomVariable):
    def __init__(self, n, p):
        self.n = n
        self.p = p
        self.mean = n * p
        self.variance = n * p * (1 - p)

    def generate(self, scale=1):
        return np.random.binomial(scale, self.p, self.n)


class Uniform(RandomVariable):
    def __init__(self, a, b, var_type='continuous'):
        self.a = a
        self.b = b
        self.var_type = var_type

        if self.var_type == 'discrete':
            self.mean = (a + b) / 2
            self.variance = ((b - a + 1) ** 2 - 1) / 12
        else:
            self.mean = (a + b) / 2
            self.variance = (b - a) ** 2 / 12

    def generate(self, n):
        if self.var_type == 'discrete':
            return np.random.randint(self.a, self.b, n)
        else:
            return np.random.uniform(self.a, self.b, n)


class Gamma(RandomVariable):
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        self.mean = alpha / beta
        self.variance = alpha / beta ** 2

    def generate(self, n):
        return np.random.gamma(self.alpha, self.beta, n)


class Beta(RandomVariable):
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        self.mean = alpha / (alpha + beta)
        self.variance = alpha * beta / ((alpha + beta) ** 2 * (alpha + beta + 1))

    def generate(self, n):
        return np.random.beta(self.alpha, self.beta, n)


class Poisson(RandomVariable):
    def __init__(self, rate):
        self.rate = rate
        self.mean = rate
        self.variance = rate

    def generate(self, n):
        return np.random.poisson(self.rate, n)
