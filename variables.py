from copy import deepcopy
import sympy

class Variables:

  # time - tuple of (name, time range)
  # dependents - list of (name, initial value)
  # constants - list of (name, value)
  def __init__(self, time, dependents, constants):
    self.symbols = {}
    self.values = {}

    self.__initialize_time(time)
    self.__initialize_dependents(dependents)
    self.__initialize_constants(constants)

  def __initialize_time(self, time):
    time_name = time[0]
    time_range = time[1]
    time_symbol = sympy.symbols(time_name)

    self.time = time_name
    self.symbols[time_name] = time_symbol
    self.values[time_name] = time_range

  def __initialize_dependents(self, dependents):
    dependent_names, dependent_values = zip(*dependents)
    self.dependents = dependent_names
    self.__initialize_variable_set(dependent_names, dependent_values)

  def __initialize_constants(self, constants):
    constant_names, constant_values = zip(*constants)
    self.constants = constant_names
    self.__initialize_variable_set(constant_names, constant_values)

  def __initialize_variable_set(self, names, values):
    symbols = self.__generate_symbols(names)
    for name, symbol in zip(names, symbols):
      self.symbols[name] = symbol
    for name, value in zip(names, values):
      self.values[name] = value

  def __generate_symbols(self, names):
    symbols = []
    for name in names:
      symbols.append(sympy.symbols(name))
    return symbols

  def get_dependent_subs(self):
    return self.__get_subs(self.dependents)

  def get_constant_subs(self):
    return self.__get_subs(self.constants)

  def __get_subs(self, variable_set):
    subs = []
    for variable in variable_set:
      subs.append( (self.symbols[variable], self.values[variable]) )
    return subs

  def __getitem__(self, item):
    return self.symbols[item]
