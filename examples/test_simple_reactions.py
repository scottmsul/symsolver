import numpy as np
import matplotlib.pyplot as pl
from sympy import *
from processes import hydrogen

import sys
sys.path.append('../symsolver')
from variables import Variables
from solver import Solver

time = ('t', np.logspace(5.0,30.0,1000))
dependents = [('HI', 0.5), ('HII', 0.5), ('e', 0.5)]
constants = [('n', 1.0), ('T', 1e4)]
v = Variables(time, dependents, constants)
solver = Solver(v)
solver.add_process(hydrogen.recombination(v))
solver.add_process(hydrogen.collisional_ionization(v))

time = v.values['t']
y = solver.solve()

pl.loglog(time, y[:,1])
pl.show()
