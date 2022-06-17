class Node:
    def __init__(self, *children, name='x', value=None):
        self.children = children
        self.name = name
        self.value = value
        self.__leaves = None

    def __repr__(self):
        return f'Node<{self.name}, {len(self.children)}, {self.leaves}>'

    def __str__(self):
        if self.is_leaf():
            return f'{self.name}'
        return f'({self.name} {" ".join(str(c) for c in self.children)})'

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

    def is_leaf(self):
        return len(self.children) == 0

    @property
    def leaves(self):
        if self.__leaves is None:
            self.__leaves = count_leaves(self)
        return self.__leaves


def nleaves(n, bfs):
    for b in bfs:
        yield from _nleaves(n, b, bfs)

def _nleaves(n, rbf, bfs):
    if n == 1:
        yield Node()

    elif rbf == 1:
        yield from nleaves(n, bfs)

    else:
        for i in range(1, n - rbf + 2):
            for r in nleaves(i, bfs):
                for l in _nleaves(n - i, rbf - 1, bfs):
                    if rbf > 2:
                        yield Node(*l.children, r, name = 'f')
                    else:
                        yield Node(l, r, name = 'f')

def count_leaves(n):
    if len(n.children) == 0:
        return 1

    return sum(count_leaves(c) for c in n.children)

snleaves = lambda *args, **kwargs: set(nleaves(*args, **kwargs))