from operator import add, sub, mul, itruediv, pow as _p, neg
from math import factorial

def pow(a, b):
    return float(a) ** b

def div(a, b):
    return itruediv(a, b)


root = lambda n, r: n ** (1 / r)

arith_ops = (add, sub, mul, div, pow)