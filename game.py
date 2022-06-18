#!/usr/bin/env python

from lib2to3.pgen2.token import COMMA
import random
from re import M
import solv
import operators
import argparse
import evaluator
import parse

def parse_function(argv):
    name, *rest = argv
    res = eval(" ".join(rest))

    if isinstance(res, tuple):
        func, maxv = res
        return operators.Function(name, func, max_applications=maxv)

    else:
        func = operators.Function(name, res)
        if func.argcount == 1:
            raise GameException("unary function needs to be accompanied with maximum number of applications")
        return func


class GameException(Exception): pass


class Command:
    def __init__(self, commands, args=(), help='N/A', parse=lambda x: x):
        self.commands = commands
        self.args = args
        self.help = help
        self._parse = parse

    def parse(self, argv):
        try:
            return self._parse(argv)
        
        except GameException:
            raise

        except Exception as e:
            raise GameException(f"Error in parsing command '{self.commands[0]}': {e}")

    def usage(self):
        return f'[{" | ".join(self.commands)}]{(" " if len(self.args) else "") + " ".join(self.args)}:\n    {self.help}'

    def __contains__(self, v):
        return v in self.commands


class Config:
    def __init__(self, n=4, lower=1, upper=10, target=24, ops=operators.arith_ops):
        self.n = n
        self.lower = lower
        self.upper = upper
        self.target = target
        self.ops = ops

    def opstrs(self):
        for f in self.ops:
            if f.argcount == 1:
                yield f'{f} -- apply at most {f.max_applications} times'
            
            else:
                yield str(f)

    def __str__(self):
        return f"n: {self.n}\n" \
               f"target: {self.target}\n" \
               f"lower: {self.lower}\n" \
               f"upper: {self.upper}\n" \
               "ops:\n    " + '\n    '.join(self.opstrs())

int_parse = lambda args: int(args[0])
COMMANDS = {
    "new-set": Command(
        ("generate", "gen", ""), 
        help="generate a random new set of numbers (guaranteed to have solutions)"
    ),

    "set-ns": Command(
        ("set-ns", "set", "make", "m"),
        args=("<NUMBERS>",),
        help="set the current set to NUMBERS",
        parse=lambda argv: tuple(int(c) for c in argv)
    ),
    
    "solve": Command(
        ("solve", "solutions", "s"),  
        help="solve the current set or"
    ),

    "set-number": Command(
        ("set-number", "numbers", "n"), 
        args=("<NUMBER>",), 
        help="set the number of numbers",
        parse=int_parse
    ),
    
    "set-target": Command(
        ("set-target", "target", "t"), 
        args=("<NUMBER>",), 
        help="set the target number",
        parse=int_parse
    ),
    
    "set-lower": Command(
        ("set-lower", "lower", "l"), 
        args=("<NUMBER>",), 
        help="set the lower bound of the possible numbers",
        parse=int_parse
    ),
    
    "set-upper": Command(
        ("set-upper", "upper", "u"), 
        args=("<NUMBER>",), 
        help="set the upper bound of the possible numbers",
        parse=int_parse
    ),

    "add-op": Command(
        ("add-op", "new-op", "op", "o"),
        args=("<NAME: STR>", "<OP: LAMBDA>"),
        help="create a new operator with name STR and function OPERATOR",
        parse=parse_function
    ),

    "remove-op": Command(
        ("remove-op", "rm-op", "rmop", "r"),
        args=("<NAME: STR>",),
        help="remove the operator NAME from the list of operators",
        parse=lambda argv: argv[0]
    ),

    "show-config": Command(
        ("show-config", "config", "status", "c"), 
        help="show the current configuration"
    ),

    "evaluate": Command(
        ("evaluate", "eval", "e"),
        args=("<EXPR>",),
        help="evaluate the expression and print the result",
        parse=lambda argv: ' '.join(argv)
    ),

    "quit": Command(("quit", "q"), help="quit"),

    "help": Command(("help", "h"), help="print this help message")
}

USAGE = "\n\n".join(c.usage() for c in COMMANDS.values())


nrandom = lambda n, l, u: tuple(random.randint(l, u) for _ in range(n))


def generate(config):
    while not len(
        s := set(solv.solve(
            ns := nrandom(config.n, config.lower, config.upper),
            target=config.target,
            ops=config.ops
        ))
    ): pass

    return ns, s


def play(config):
    ns, s = generate(config)
    while (command := input(f'{config.target}: {ns}> ').lower()) not in COMMANDS["quit"]:
        try:
            c, *args = command.split(" ")
            if c in COMMANDS["new-set"]:
                ns, s = generate(config)

            elif c in COMMANDS["set-ns"]:
                ns = COMMANDS["set-ns"].parse(args)
                s  = set(solv.solve(ns, target=config.target, ops=config.ops))

            elif c in COMMANDS["solve"]:
                print(*s, sep='\n')
                print(f'{len(s)} solutions')

            elif c in COMMANDS["set-number"]:
                config.n = COMMANDS["set-number"].parse(args)
                ns, s = generate(config)

            elif c in COMMANDS["set-target"]:
                config.target = COMMANDS["set-target"].parse(args)
                s  = set(solv.solve(ns, target=config.target, ops=config.ops))
                if len(s) == 0:
                    ns, s = generate(config)

            elif c in COMMANDS["set-lower"]:
                config.lower = COMMANDS["set-lower"].parse(args)
                if any(x <= config.lower for x in ns):
                    ns, s = generate(config)

            elif c in COMMANDS["set-upper"]:
                config.upper = COMMANDS["set-upper"].parse(args)
                if any(x >= config.upper for x in ns):
                    ns, s = generate(config)

            elif c in COMMANDS["add-op"]:
                config.ops += COMMANDS["add-op"].parse(args),
                s  = set(solv.solve(ns, target=config.target, ops=config.ops))

            elif c in COMMANDS["remove-op"]:
                n = COMMANDS["remove-op"].parse(args)
                config.ops = tuple(o for o in config.ops if o.name != n)
                s  = set(solv.solve(ns, target=config.target, ops=config.ops))

            elif c in COMMANDS["evaluate"]:
                e = COMMANDS["evaluate"].parse(args)
                r = evaluator.safe_eval_tree(parse.treeify(e, config.ops))
                print(r)

            elif c in COMMANDS["show-config"]:
                print(config)

            elif c in COMMANDS["help"]:
                print(USAGE)

            else:
                print("unrecognized command... type 'help' to see all available commands")

        except GameException as e:
            print(e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', default=4, type=int, help='how many numbers')
    parser.add_argument('-l', '--lower', default=1, type=int,
                        help='lower bound for the domain of numbers')
    parser.add_argument('-u', '--upper', default=10, type=int,
                        help='upper bound for the domain of numbers')
    parser.add_argument('-t', '--target', default=24, type=int,
                        help='target value for the expressions')

    args = parser.parse_args()

    try:
        play(Config(**vars(args)))

    except (EOFError, KeyboardInterrupt):
        return 0


if __name__ == '__main__':
    raise SystemExit(main())
