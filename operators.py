from operator import add, sub, mul, itruediv, pow, neg
from math import factorial

def div(a, b):
    return itruediv(a, b)


root = lambda n, r: n ** (1 / r)

arith_ops = (add, sub, mul, div, pow)