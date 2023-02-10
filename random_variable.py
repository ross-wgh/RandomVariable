import numpy as np


class RandomVariable:

    # Every random variable has a mean and variance
    # The calculation for these two parameters will be different for each subclass
    def __init__(self, mean, variance):
        self.mean = mean
        self.variance = variance

    def __add__(self, other):
        if type(other) == int:
            return self.__class__(self.mean + other, self.variance)
        elif type(other) == type(self):
            # Need to figure out how to implement covariance
            return self.__class__(self.mean + other.mean, self.variance + other.variance)
        elif issubclass(self.__class__, RandomVariable) and issubclass(other.__class__, RandomVariable):
            return RandomVariable(self.mean + other.mean, self.variance + other.variance)

        # Need else statement to raise exception if you try to add/sub/mult/divide by non-numeric or non-random var

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if type(other) == int:
            return self.__class__(self.mean - other, self.variance)
        elif type(other) == type(self):
            # Need to figure out how to implement covariance
            return self.__class__(self.mean - other.mean, self.variance + other.variance)
        elif issubclass(self.__class__, RandomVariable) and issubclass(other.__class__, RandomVariable):
            return RandomVariable(self.mean - other.mean, self.variance + other.variance)

        # Need else statement to raise exception if you try to add/sub/mult/divide by non-numeric or non-random var

    def __mul__(self, other):
        if type(other) == int:
            return self.__class__(self.mean * other, self.variance * other ** 2)
        elif issubclass(self.__class__, RandomVariable) and issubclass(other.__class__, RandomVariable):
            return RandomVariable(self.mean * other.mean, (self.variance + self.mean ** 2) *
                                  (other.variance + other.mean ** 2) - self.mean ** 2 * other.mean ** 2)

        # Need else statement to raise exception if you try to add/sub/mult/divide by non-numeric or non-random var

    def __rmul__(self, other):
        # is this bad coding practice? look up examples online
        return self.__mul__(other)

    # Variance Behavior is likely  incorrect with multiple random variables, need to do derivation of Var(X/Y)
    def __truediv__(self, other):
        if type(other) == int:
            return self.__class__(self.mean / other, self.variance / other ** 2)
        elif issubclass(self.__class__, RandomVariable) and issubclass(other.__class__, RandomVariable):
            return RandomVariable(self.mean / other.mean, (self.variance + self.mean ** 2) *
                                  (other.variance + other.mean ** 2) - self.mean ** 2 * other.mean ** 2)

    def __str__(self):
        if type(self).__name__ != 'RandomVariable':
            return f"This is a {type(self).__name__} random variable with mean: {self.mean} and variance: {self.variance}"
        else:
            return f"This is a random variable with mean: {self.mean} and variance: {self.variance}"

    def __eq__(self, other):
        if type(other) == type(self):
            if self.mean == other.mean and self.variance == other.variance:
                return True
        else:
            return False


class Normal(RandomVariable):
    def __init__(self, mean, variance):
        self.mean = mean
        self.variance = variance

    def generate(self, n):
        return np.random.normal(self.mean, self.variance, n)

'''    def __eq__(self, other):
        if type(other) == Normal:
            if self.mean == other.mean and self.variance == other.variance:
                return True
        else:
            return False

    def __add__(self, other):
        if type(other) == int:
            return Normal(self.mean + other, self.variance)
        elif type(other) == Normal:
            #Need to figure out how to implement covariance
            return Normal(self.mean + other.mean, self.variance + other.variance)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if type(other) == int:
            return Normal(self.mean - other, self.variance)
        elif type(other) == Normal:
            # Need to figure out how to implement covariance
            return Normal(self.mean - other.mean, self.variance - other.variance)

    def __mul__(self, other):
        if type(other) == int:
            return Normal(self.mean * other, self.variance * other ** 2)
        elif other == Normal(0, 1) and self == Normal(0, 1):
            return ChiSquare(1)
        elif type(other) == Normal:
            return Normal(0, 0)

    def __rmul__(self, other):

        # is this bad coding practice? look up examples online
        return self.__mul__(other)

    def __truediv__(self, other):
        if type(other) == int:
            return Normal(self.mean / other, self.variance / other ** 2)
        elif type(other) == Normal:
            return Normal(0, 0)

    def __str__(self):
        return f"This is a Normal Random variable with mean: {self.mean} and variance: {self.variance}"'''


class ChiSquare(Normal):
    def __init__(self, df):
        self.df = df
        self.mean = df
        self.variance = 2 * df

    def __mul__(self, other):
        if other == Normal(0, 1):
            return ChiSquare(self.df + 1)
        else:
            return Normal.__mul__(self, other)
        # A chi-sq times a chi-sq is not a chi-sq
        # Ergo - need to make generalized form to account for this
        '''
                elif type(other) == type(self):
            return ChiSquare(self.df * other.df)
        '''

    def __rmul__(self, other):
        return self.__mul__(other)


class Binomial(RandomVariable):
    def __init__(self, n, p):
        super().__init__()
        self.n = n
        self.p = p

    def generate(self, scale=1):
        return np.random.binomial(scale, self.p, self.n)


class Uniform(RandomVariable):
    def __init__(self, a, b, var_type='continuous'):
        super().__init__()
        self.a = a
        self.b = b
        self.var_type = var_type

        # These stats are only for continuous
        self.mean = 1 / (b - a)
        self.variance = 2 / 12

    def generate(self, n):
        if self.var_type == 'discrete':
            return np.random.randint(self.a, self.b, n)
        else:
            return np.random.uniform(self.a, self.b, n)


class Gamma(RandomVariable):
    def __init__(self, alpha, beta):
        super().__init__()
        self.alpha = alpha
        self.beta = beta
        self.mean = alpha / beta
        self.variance = alpha / beta ** 2

    def generate(self, n):
        return np.random.gamma(self.alpha, self.beta, n)


class Poisson(RandomVariable):
    def __init__(self, rate):
        super().__init__()
        self.rate = rate
        self.mean = rate
        self.variance = rate

    def generate(self, n):
        return np.random.poisson(self.rate, n)


if __name__ == "__main__":
    # X = Normal(1, 2).generate(100)
    # Y = Normal(1, 3).generate(100)
    X = Normal(1, 2)
    Y = Normal(2, 4)
    Z = Normal(4, 2)
    print(X.mean, X.variance)
    print(X)
    X2 = X * 2
    print(X2.mean, X2.variance)
    print(X2)

    X2 = 2 * X
    print(X2.mean, X2.variance)
    print(X2)

    XY = X * Y

    print(XY.mean, XY.variance)
    print(XY)

    Xhalf = X / 2
    XYhalf = Xhalf / Y
    print(Xhalf.mean, Xhalf.variance)
    print(Xhalf)
    print(XYhalf.mean, XYhalf.variance)

    print(X + Y + Z)
    print('hi')
    print(ChiSquare(2) + Normal(0, 1))
    print(Normal(0, 1) + ChiSquare(2))

    print(issubclass(ChiSquare, RandomVariable))
    print(issubclass(Normal(0, 1).__class__, RandomVariable))
