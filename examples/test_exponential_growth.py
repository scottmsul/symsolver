import numpy as np
import matplotlib.pyplot as pl
from sympy import *

import sys
sys.path.append('../symsolver/')
from variables import Variables
from solver import Solver

time = ('t', np.logspace(1.0,3.0,1000))
dependents = [('x', 1.0)]
constants = [('tau', 5.0)]
v = Variables(time, dependents, constants)
solver = Solver(v)
solver.add_process({
  'x': v['x']/v['tau']
  })

time = v.values['t']
y = solver.solve()

pl.semilogy(time, y[:,0])
pl.show()
