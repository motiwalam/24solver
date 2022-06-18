from functools import reduce
from itertools import groupby
from trees import Node
import re

class ParseException(Exception): pass

dedup = lambda s, cs = (' ',): reduce(
    lambda a, b: a + (b[0] if b[0] in cs else ''.join(b[1])),
    groupby(s),
    ''
)

pythonify = lambda s: re.sub(
    r'[^\(\)0-9 ]+',
    lambda m: f"'{m.string[m.start():m.end()]}'",
    s
).replace(' ', ',')


tuplify = lambda s: eval(pythonify(dedup(s)))

def _treeify(s, ops):
    if not isinstance(s, tuple):
        return Node(name=s, value=s)
    
    f, *r = s
    try:
        func = ops[f, len(r)]
        return Node(*(_treeify(c, ops) for c in r), name=func.name, value=func)
    
    except KeyError:
        raise ParseException(f"no operator found for {len(r)}-ary {f}")

    except SyntaxError as e:
        raise ParseException(f"syntax error: {e}")

    except Exception as e:
        raise ParseException(f"an error occurred while parsing: {e}")
        


treeify = lambda s, ops: _treeify(tuplify(s), {(f.name, f.argcount): f for f in ops})