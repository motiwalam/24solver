# 24solver
a solver for the generalized game of 24

### what do you mean generalized?
In the [original game of 24](https://www.24game.com), you were to choose `4` numbers and combine them with the operations `+`, `-`, `/`, `*` to produce the value `24`.

This solver parameterizes all three of the highlighted options. 

* Instead of `4` numbers, you can have `n` numbers. 
* Instead of targeting the value `24`, you can target any value `t`
* Instead of only being able to use the operators `+`, `-`, `/`, `*`, you can use and define any set of operators that take any number of operands

## Usage
The file `game.py` can be executed to provide a front end to the solver. 
Here, you can configure the parameters, add and remove operators, and just play the game.
Execute `game.py` and type `help` to see all of the available commands.

```bash
./game.py
# if you have rlwrap installed
# rlwrap ./game.py
```

### using the solver programmatically
The solver is exposed under a single function `solve` in the `solv.py` module.
`solve` has the signature:
```python
def solve(ns: tuple[number], target: number = 24, ops: tuple[Operator] = operators.arith_ops) -> Generator[Node]
```
`Operator` is a class defined in the `operators.py` module. It has the signature:
```python
class Operator:
  def __init__(self, name: str, f: Callable, max_applications: int = None)
```
`operators.arith_ops` is a tuple of the operators `add`, `sub`, `mul`, `div`, and `pow`.

`Node` is a class defined in the module `trees.py`. Calling `str` on it will produce a string representing it in s-expression syntax.

### example usage
#### default parameters
```python
import solv
solns = solv.solve((1, 2, 3, 4))
print(len(set(solns)))
# 307
```
#### adding a custom operator
```python
import solv
import operators
root = operators.Operator('root', lambda n, r: n ** (1/r))
solns = solv.solve((1, 2, 3, 4), ops=operators.arith_ops + (root,))
print(len(set(solns)))
# 367
```
#### using a different target
```python
import solv
solns = tuple(solv.solve((1, 2, 3, 4), target=36))
print(len(solns))
# 85
print(solns[0])
# (* (+ (^ 2 3) 1) 4)
```
#### using operators with more than two operands
```python
import solv
import operators
avg = operators.Operator('avg', lambda a, b, c: (a + b + c) / 3)
solns = solv.solve((6, 4, 3, 2), ops=operators.arith_ops + (avg,))
print(*set(solns), sep='\n')
# ...
# (avg 6 (^ 4 3) 2)
# ...
```
### A note on unary operators
In the signature for the `Operator` object, you saw a parameter called `max_applications`. This note discusses this parameter and why it is needed.

This solver works by generating all possible expressions for a given set of numbers and operators, and then filters them for ones that evaluate to the correct value.

When unary operators are allowed, this becomes impossible because the set of possible expressions becomes infinite. To see why, note that `-5`, `--5`, `---5`, `---------------------5` are all valid expressions that only use one number.

Thus, any unary operators are required to specify a maximum number of times the solver is allowed to apply it on a single node. For example, the negation operator above should only ever be applied once, applying it more than that never makes sense.

Even with this restriction, adding unary operators makes this process take a lot, lot longer. For example, just adding a single unary operator to the default set increases the set of possible expressions by a factor of 128.

### A note on the uniqueness of solutions
This solver has no notion of commutativity and associativity of operations. It considers `8 * 3` and `3 * 8` distinct and will generate both of them.

It also does not respect repeated numbers in the input set. Thus, the set of possible expressions for input `a, a, b, c` will generate every unique expression exactly twice.

### A note on variadic operators
Currently, variadic operators will not work correctly. This is because a function `lambda *args: ...` is considered to take one argument, and so the solver will only ever give it one argument.
