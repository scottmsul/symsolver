import numpy as np
from sympy import lambdify, diff, S
from scipy.integrate import ode

class Solver:

  def __init__(self, variables):
    self.variables = variables
    self.__initialize_derivatives()
    self.__initialize_solver()

  def __initialize_derivatives(self):
    self.symbolic_derivatives = {}
    for dependent in self.variables.dependents:
      self.symbolic_derivatives[dependent] = S.Zero

  def __initialize_solver(self):
    self.ode_solver = ode(f=self.__derivatives, jac=self.__jacobian)
    self.ode_solver.set_integrator("vode", method="bdf")

  def add_process(self, process):
    for dependent, term in process.iteritems():
      self.symbolic_derivatives[dependent] += term

  def solve(self):
    self.__initialize_callbacks()
    return self.__solve_all_timesteps()

  def __initialize_callbacks(self):
    num_dependents = len(self.variables.dependents)
    derivatives_vector = [0] * num_dependents
    jacobian_matrix = [ [0] * num_dependents ] * num_dependents

    for dependent_index in range(num_dependents):
      dependent = self.variables.dependents[dependent_index]
      dependent_update_term = self.symbolic_derivatives[dependent]
      dependent_update_term = dependent_update_term.subs(self.variables.get_constant_subs())
      derivatives_vector[dependent_index] = dependent_update_term

      for wrt_index in range(num_dependents):
        wrt = self.variables.dependents[wrt_index]
        jacobian_update_term = diff(dependent_update_term, wrt)
        jacobian_matrix[dependent_index][wrt_index] = jacobian_update_term

    args = []
    args.append(self.variables[self.variables.time])
    args.extend(self.variables.dependents)

    self.derivatives_function = lambdify(args, derivatives_vector)
    self.jacobian_function = lambdify(args, jacobian_matrix)

  def __derivatives(self, t, y):
    derivatives = self.derivatives_function(t, *y)
    return np.array(derivatives)

  def __jacobian(self, t, y):
    jacobian = self.jacobian_function(t, *y)
    return np.array(jacobian)

  def __solve_all_timesteps(self):
    (y0, t0) = self.__get_initial_conditions()
    self.ode_solver.set_initial_value(y0, t0)

    time = self.variables.values[self.variables.time]
    num_steps = len(time)
    num_dependents = len(self.variables.dependents)
    values = np.zeros( (num_steps, num_dependents) )
    values[0, :] = y0
    steps = range(1, num_steps)
    time = time[1:]
    for (current_step, current_time) in zip(steps, time):
      current_values = self.__integrate_step(current_time)
      values[current_step, :] = current_values
    return values

  def __get_initial_conditions(self):
    time = self.variables.values[self.variables.time]
    t0 = time[0]

    num_dependents = len(self.variables.dependents)
    dependents_vector = [0] * num_dependents
    for dependent_index in range(num_dependents):
      dependent = self.variables.dependents[dependent_index]
      dependent_value = self.variables.values[dependent]
      dependents_vector[dependent_index] = dependent_value
    y0 = np.array(dependents_vector)

    return (y0, t0)

  def __integrate_step(self, current_time):
    self.ode_solver.integrate(current_time)
    if not self.ode_solver.successful():
      raise RuntimeError('The solver encountered a problem at ' + str(current_time))
    return self.ode_solver.y
