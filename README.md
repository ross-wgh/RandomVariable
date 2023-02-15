# RandomVariable Calculator
OOP Random Variable Calculator that utilizes magic methods to support mathematical operations between both native python data types and custom RandomVariable objects. Supports operations for both independent and dependent random variables.

I talk more about the motivations and the development process of this project on my [website](https://www.rosswoleben.com/projects/random-variable).
## Demo
### Working with Normal Random Variables
#### Operations with constants
```
X = Normal(3, 5)
X + 5
X - 5
X * 5
```
``` 
This is a Normal random variable with mean: 8 and variance: 25
This is a Normal random variable with mean: -2 and variance: 25
This is a Normal random variable with mean: 15 and variance: 625
```
#### Operations with another normal variable
```
Y = Normal(2, 4)
X + Y
3.5 * X + Y
```
``` 
This is a Normal random variable with mean: 5 and variance: 41.0
This is a Normal random variable with mean: 12.5 and variance: 322.25
```
### Chi-Square Random Variables
#### Using Standard Normal's to get a Chi-Square 
```
X1 = Normal(0, 1)
X2 = Normal(0, 1)
X1 * X1
X1 * X2
```
Note that X1*X1 is a Chi-Square, but X1 * X2 is just a general-form random variable
```
This is a ChiSquare random variable with mean: 1 and variance: 2
This is a random variable with mean: 0 and variance: 1
```
#### Adding Chi-Square Random Variables
```
X1 * X1 + X2 * X2
ChiSquare(2) + ChiSquare(5))
```
```
This is a ChiSquare random variable with mean: 2 and variance: 4
This is a ChiSquare random variable with mean: 7 and variance: 14
```

### Mixing Distributions
Adding and multiplying a Gamma random variable by a Beta random variable
```
g = Gamma(2, 3)
b = Beta(1, 2)
g+b
g*b
```
```
This is a random variable with mean: 1.0 and variance: 0.2777777777777778
This is a random variable with mean: 0.2222222222222222 and variance: 0.06172839506172839
```
Adding and multiplying a Uniform random variable by a Poisson random variable
```
u = rv.Uniform(1, 15)
p = rv.Poisson(3)
```
```
This is a random variable with mean: 19.0 and variance: 68.33333333333333
This is a random variable with mean: 16.0 and variance: 306.33333333333326
```
### Covariance/Correlation (Non-Independent) Operations
Use the ```add_cov``` and ```sub_cov``` methods to implement covariance structures to addition and subtraction calculations.
Using X and Y as defined above, a covariance of 3 is equivalent to using a correlation of .15:

```
# 2X + Y; COV(X,Y) = 3 <==> COR(X,Y) = 15
Z1 = (2*X).add_cov(Y, covariance=3)
Z1
# 2X - Y; COV(X,Y) = 3 <==> COR(X,Y) = 15
Z2 = (2 * X).sub_cov(Y, covariance=3)
Z2
```
```
This is a random variable with mean: 8 and variance: 128
This is a random variable with mean: 4 and variance: 104
```

### Generating Values from Distributions
Furthermore, each distribution has a 
```.generate(sample_size)```
method that calls numpy's random subpackage to generate values from the defined distribution.

A run of ```.generate()``` on a standard normal
```
Normal(0, 1).generate(10)
```
```
[ 1.03501459 -1.57100292 -0.09806292  2.00850966 -0.44300292 -1.24323369
 -0.71024497 -0.49864488  1.38255299  0.31290998]
```
