from operator import add, sub, mul, itruediv, neg
from math import factorial
from inspect import signature


def names(n):
    chars = "xyz"
    numc = len(chars)
    for i in range(n):
        idx = i % numc
        subscript = '' if i < numc else str(i // numc)
        yield chars[idx] + subscript


class Function:
    def __init__(self, name, f, max_applications=None):
        self.name = name
        self.f = f
        self.__argcount = None
        self.max_applications = max_applications

    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)

    def __str__(self):
        return f'{self.name}({", ".join(names(self.argcount))})'

    @property
    def argcount(self):
        if self.__argcount is None:
            self.__argcount = len(signature(self.f).parameters)

        return self.__argcount


add = Function('+', add)
sub = Function('-', sub)
mul = Function('*', mul)
div = Function('/', itruediv)
pow = Function('^', lambda a, b: float(a) ** b)
neg = Function('-', neg)
root = Function('root', lambda n, r: n ** (1 / r))
fact = Function('!', factorial, max_applications=1)

arith_ops = (add, sub, mul, div, pow)