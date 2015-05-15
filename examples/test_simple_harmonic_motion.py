import numpy as np
import matplotlib.pyplot as pl
from sympy import *

import sys
sys.path.append('../symsolver')
from variables import Variables
from solver import Solver

time = ('t', np.logspace(1.0,3.0,1000))
dependents = [('x', 1.0), ('y', 0.0)]
constants = [('tau', 500)]
v = Variables(time, dependents, constants)

solver = Solver(v)
solver.add_process({
  'x': v['y']/sqrt(v['tau']),
  'y': -v['x']/sqrt(v['tau'])
  })

time = v.values['t']
y = solver.solve()
print y[:,0]

pl.plot(time, y[:,0])
pl.show()
