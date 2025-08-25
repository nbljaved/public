import sys
import json

def do_add(env, args):
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left + right

def do_abs(env, args):
    assert len(args) == 1
    val = do(env, args[0])
    return abs(val)

# Looking up variables when we need their values is straightforward. We check
# that we have a variable name and that the name is in the environment, then
# return the stored value:
def do_get(env, args):
    assert len(args) == 1
    assert isinstance(args[0], str)
    assert args[0] in env, f"Unknown variable {args[0]}"
    return env[args[0]]

# To define a new variable or change an existing one, we evaluate an expression
# and store its value in the environment:
def do_set(env, args):
    assert len(args) == 2
    assert isinstance(args[0], str)
    value = do(env, args[1])
    env[args[0]] = value
    return value

# We need to add one more function to make this all work. Our programs no longer
# consist of a single expression; instead, we may have several expressions that
# set variables’ values and then use them in calculations. To handle this, we
# add a function do_seq that runs a sequence of expressions one by one. This
# function is our first piece of control flow: rather than calculating a value
# itself, it controls when and how other expressions are evaluated. Its
# implementation is:
def do_seq(env, args):
    assert len(args) > 0
    for item in args:
        result = do(env, item)
    return result


OPS = {
    name.replace('do_', ''): func
    for name, func in globals().items()
    if name.startswith('do_') and callable(func)
}

def do(env, expr):
    # Integers evaluate to themselves.
    if isinstance(expr, int):
        return expr

     # Lists trigger function calls.
    assert isinstance(expr, list)
    assert expr[0] in OPS, f"Unknown operation {expr[0]}"
    func = OPS[expr[0]]
    return func(env, expr[1:])

def main():
    assert len(sys.argv) == 2, "Usage: expr.py filename"
    with open(sys.argv[1], "r") as reader:
        program = json.load(reader)
    env = {} # initialize the environment
    result = do(env, program)
    print(f"=> {result}")

if __name__ == "__main__":
    main()
