import sys
import json

#from pprint import pprint

def do_add(env, args):
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left + right

def do_abs(env, args):
    assert len(args) == 1
    val = do(env, args[0])
    return abs(val)

# Changed !
def do_get(env, args):
    # pprint('do_get')
    # pprint(f'env: {env}')
    # pprint(f'args: {args}')
    assert len(args) == 1
    assert isinstance(args[0], str)
    name = args[0]
    for d in reversed(env):
        if name in d:
            return d[name]
    raise Exception(f'nothing defined with name: {name}')

# Changed !
def do_set(env, args):
    assert len(args) == 2
    assert isinstance(args[0], str)
    value = do(env, args[1])
    env[-1][args[0]] = value
    return value

def do_seq(env, args):
    assert len(args) > 0
    for item in args:
        result = do(env, item)
    return result


def do_func(env, args):
    assert len(args) == 2
    params = args[0]
    body = args[1]
    return ['func', params, body]

# NOTE: How the above function just checks that function has the correct shape
# and just returns the same value as earlier.

# This is what we mean when we say that a function:
# saves instructions for later use.

def do_call(env, args):
    # set up the call
    assert len(args) >= 1
    name = args[0]
    arguments = [do(env, a) for a in args[1:]]

    # find the function
    func = do_get(env, [name])
    # NOTE :: In the above, if I wrote list(name), then
    # we would get ['a', 'b', 'c'] for the name='abc' !!
    assert isinstance(func, list) and (func[0] == 'func')
    params, body = func[1], func[2]
    assert len(arguments) == len(params)

    # Run in new environment
    env.append(dict(zip(params, arguments))) # Noice
    result = do(env, body)
    env.pop()

    # Report
    return result

def do_repeat(env, args):
    # ['repeat', times, body]
    assert len(args) == 2

    times = do(env, args[0])
    body = args[1]

    for _ in range(times):
        do(env, body)

def do_print(env, args):
    # ['print', thing]
    assert len(args) == 1
    value = do(env, args[0])
    print(value)

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
    # pprint(f'Calling func: {expr[0]}')
    # pprint(f'with args: {expr[1:]}')
    return func(env, expr[1:])

def main():
    assert len(sys.argv) == 2, "Usage: expr.py filename"
    with open(sys.argv[1], "r") as reader:
        program = json.load(reader)
    # NOTE: list(dict()) => []
    env = [dict()] # Changed !

    result = do(env, program)
    print(f"=> {result}")

if __name__ == "__main__":
    main()
