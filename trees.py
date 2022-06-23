from itertools import product
from functools import cached_property

class Node:
    def __init__(self, *children, name='x', value=None):
        self.children = children
        self.name = name
        self.value = value

    def __repr__(self):
        return f'Node<{self.name}, {self.arity}, {self.numleaves}>'

    def __str__(self):
        if self.is_leaf:
            return f'{self.name}'

        if self.arity == 2:
            return f'({self.children[0]} {self.name} {self.children[1]})'

        return f'({self.name} {" ".join(str(c) for c in self.children)})'

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

    @property
    def arity(self):
        return len(self.children)

    @property
    def is_leaf(self):
        return self.arity == 0

    @cached_property
    def numleaves(self):
        return count_leaves(self)

# generate all trees with n leaves where the number of children 
# of non leaf node comes from the set a
def nleaves(n, a):
    for b in a:
        yield from _nleaves(n, b, a)

# a more specific version of nleaves, where the number of children
# for the root node is fixed to be k
def _nleaves(n, k, a):
    if   n == 1: yield Node()
    elif k == 1: yield from nleaves(n, a)
    else:
        for i in range(1, n - k + 2):
            for r, l in product(nleaves(i, a), _nleaves(n - i, k - 1, a)):
                if k == 2: yield Node(l, r, name='f')
                else:      yield Node(*l.children, r, name='f')


count_leaves = lambda t: (len(t.children) == 0) + sum(map(count_leaves, t.children))
snleaves = lambda *args, **kwargs: set(nleaves(*args, **kwargs))