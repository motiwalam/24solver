from trees import nleaves, Node
from itertools import groupby, product, permutations
from more_itertools import flatten
from functools import reduce, partial
from evaluator import safe_eval_tree
import operators
import sys

foldr = lambda func, xs, initial: reduce(lambda x, y: func(y, x), reversed(xs), initial)
optable = lambda ops: {k: tuple(g) for k, g in groupby(ops, lambda v: v.argcount)}
apply_unary = partial(foldr, lambda f, g: Node(g, name=f.name, value=f))

def possible_unary_apps(funcs):
    for combo in product(*(range(f.max_applications + 1) for f in funcs)):
        fs = flatten((f,) * i for f, i in zip(funcs, combo))
        yield from permutations(fs)


def possible_ops(t, optable):
    if t.is_leaf:
        yield t

    else:
        for o, *cs in product(
            optable[len(t.children)],
            *(possible_ops(c, optable) for c in t.children)
        ): yield Node(*cs, name=o.name, value=o)


def with_leaves(t, l):
    if t.is_leaf:
        v = l.pop()
        return Node(name=v, value=v)

    else:
        return Node(*(with_leaves(c, l) for c in t.children), name=t.name, value=t.value)


def with_unary(t, unarys):
    for apps, *cs in product(
        unarys,
        *(with_unary(c, unarys) for c in t.children)
    ): yield apply_unary(apps, Node(*cs, name=t.name, value=t.value))

        
def possible_trees(t, n, optable):
    unarys = set(possible_unary_apps(optable.get(1, [])))
    for tr, ls in product(possible_ops(t, optable), permutations(n)):
        v = with_leaves(tr, list(ls))
        yield from with_unary(v, unarys) if unarys else (v,)


def gen_exprs(n, ops):
    table = optable(ops)
    trees = nleaves(len(n), tuple(k for k in table.keys() if k != 1))

    for t in trees:
        yield from possible_trees(t, n, table)


solve = lambda ns, target=24, ops=operators.arith_ops: (t for t in gen_exprs(ns, ops) if safe_eval_tree(t) == target)

if __name__ == "__main__":
    target, ops_str, *ns = sys.argv[1:]
    target, ns = int(target), list(map(int, ns))

    ops = [o for o in operators.arith_ops if o.name in ops_str]
    
    try:
        for soln in solve(ns, target, ops):
            print(soln)
    except KeyboardInterrupt as e:
        print()
        raise SystemExit(0)
