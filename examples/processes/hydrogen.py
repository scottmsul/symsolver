from sympy import *

# H+ + e -> H
def recombination(v):
  rate_coefficient = 6.28e-11 * (v['T'] ** -0.5) * (v['T']/1e3) ** -0.2 * (1 + (v['T'] / 1e6) ** 0.7) ** -1
  current_rate = v['HII'] * v['e'] * v['n'] * rate_coefficient
  process = {
    'HII': -1 * current_rate,
    'e': -1 * current_rate,
    'HI': current_rate,
  }
  return process

# H + e -> H+ + 2e
def collisional_ionization(v):
  rate_coefficient = 5.85e-11 * (v['T'] ** 0.5) * (1 + (v['T']/1e5) ** 0.5) ** -1 * exp(-1.578e5 / v['T'])
  current_rate = v['HI'] * v['e'] * v['n'] * rate_coefficient
  process = {
    'HII': current_rate,
    'e': current_rate,
    'HI': -1 * current_rate,
  }
  return process
