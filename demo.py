import random_variable as rv

if __name__ == "__main__":

    print("**NORMAL DEMONSTRATION**")
    X = rv.Normal(3, 5)
    print(X + 5)
    print(X - 5)
    print(X * 5)

    Y = rv.Normal(2, 4)

    print(X + Y)
    print(3.5 * X + Y)

    print("**CHI-SQUARE DEMONSTRATION**")
    X1 = rv.Normal(0, 1)
    X2 = rv.Normal(0, 1)

    # A Standard Normal squared is a Chi-Square with 1 degree of freedom
    print(X1 * X1)

    # However, two product of two different standard normals is not
    print(X1 * X2)

    # But the sum of the two standard normals squared would be a Chi-Square with 2 degrees of freedom
    print(X1 * X1 + X2 * X2)

    # Sum of two Chi-Square is a Chi-square with the sum of the degrees of freedom
    print(rv.ChiSquare(2) + rv.ChiSquare(5))

    print("**MIXED VARIABLES DEMONSTRATION**")
    g = rv.Gamma(2, 3)
    b = rv.Beta(1, 2)

    # Gamma plus Beta and Gamma Times Beta
    print(g + b)
    print(g * b)

    u = rv.Uniform(1, 15)
    p = rv.Poisson(3)

    print(2*u + p)
    print((p - 1) * u)

    print("**COVARIANCE // CORRELATION IS NON-ZERO**")
    # Also has the ability to perform calculations when the variables are not independent

    # Re-defining variables from above
    X = rv.Normal(3, 5)
    Y = rv.Normal(2, 4)

    # The below equation is equivalent to Z = 2X + Y, where COV(X,Y) = 3 -> (Corr(X,Y) = .15)
    Z1 = (2*X).add_cov(Y, covariance=3)
    print(Z1)

    # The below equation is equivalent to Z = 2X - Y, where COV(X,Y) = 3 -> (Corr(X,Y) = .15)
    Z2 = (2 * X).sub_cov(Y, covariance=3)
    print(Z2)

    print("**GENERATING VALUES FROM THESE DISTRIBUTIONS")
    print(rv.Normal(0, 1).generate(10))
    print(rv.ChiSquare(5).generate(10))
    print(rv.Binomial(10, .5).generate())
    print(rv.Uniform(1, 10).generate(10))
    print(rv.Uniform(1, 10, 'discrete').generate(10))
    print(rv.Gamma(3, 2).generate(10))
    print(rv.Beta(3, 2).generate(10))
