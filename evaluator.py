def eval_tree(tree):
    if tree.is_leaf:
        return tree.value
    return tree.value(*(eval_tree(c) for c in tree.children))


def safe_eval_tree(tree, default=None):
    try:
        return eval_tree(tree)

    except Exception:
        return default