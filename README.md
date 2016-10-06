# symsolver
`symsolver` is a Python module for setting up ODE solvers symbolically.
To use `symsolver`, first create a list of variables representing the time, the dependent variables, and constants with initial values.
Then use `sympy` to create symbolic equations representing the update terms in the ODE.
Under the hood, `symsolver` automatically takes derivatives and creates lambda functions for the derivative term and the jacobian term.
Some example code is given in the `examples` folder.
