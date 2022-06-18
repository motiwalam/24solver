from trees import nleaves, Node
from itertools import groupby, product, permutations
from more_itertools import flatten
from functools import reduce
import operators

foldr = lambda func, xs, initial: reduce(lambda x, y: func(y, x), reversed(xs), initial)

def optable(ops):
    return {k: tuple(g) for k, g in groupby(ops, lambda v: v.argcount)}


def possible_unary_apps(funcs):
    for combo in product(*(range(f.max_applications + 1) for f in funcs)):
        fs = flatten((f,) * i for f, i in zip(funcs, combo))
        yield from permutations(fs)


def possible_ops(t, optable):
    if t.is_leaf():
        yield t

    else:
        for o in optable[len(t.children)]:
            for cs in product(*(possible_ops(c, optable) for c in t.children)):
                yield Node(*cs, name = o.name, value = o)


def with_leaves(t, l):
    if t.is_leaf():
        v = l.pop()
        return Node(name = v, value = v)

    else:
        return Node(*(with_leaves(c, l) for c in t.children), name = t.name, value = t.value)

def apply_unary(fs, node):
    return foldr(lambda f, g: Node(g, name = f.name, value = f), fs, node)

def with_unary(t, unarys):
    for apps in unarys:
        for cs in product(*(with_unary(c, unarys) for c in t.children)):
            yield apply_unary(apps, Node(*cs, name = t.name, value = t.value))
        
def possible_trees(t, n, optable):
    unarys = set(possible_unary_apps(optable.get(1, [])))
    for tr in possible_ops(t, optable):
        for ls in permutations(n):
            v = with_leaves(tr, list(ls))
            if unarys:
                yield from with_unary(v, unarys)
            else:
                yield v


def eval_tree(tree):
    if tree.is_leaf():
        return tree.value
    return tree.value(*(eval_tree(c) for c in tree.children))


def safe_eval_tree(tree, default=None):
    try:
        return eval_tree(tree)

    except Exception:
        return default

def gen_exprs(n, ops):
    table = optable(ops)
    trees = nleaves(len(n), tuple(k for k in table.keys() if k != 1))

    for t in trees:
        yield from possible_trees(t, n, table)


def solve(ns, target = 24, ops = operators.arith_ops):
    yield from (t for t in gen_exprs(ns, ops) if safe_eval_tree(t) == target)