from .tokenize_arithmetic import *

from dataclasses import dataclass

class Parsed:
    pass

@dataclass
class Number(Parsed):
    value: str

    def __call__(self):
        return self.value

class Operation(Parsed):
    def __call__(self):
        return [self.op, self.left(), self.right()]

@dataclass
class Add(Operation):
    left: Parsed
    right: Parsed
    op: str = '+'

@dataclass
class Subtract(Operation):
    left: Parsed
    right: Parsed
    op: str = '-'

@dataclass
class Multiply(Operation):
    left: Parsed
    right: Parsed
    op: str = '*'

@dataclass
class Divide(Operation):
    left: Parsed
    right: Parsed
    op: str = '*'

def find_bracket_end(tokens, bracket_open_index):
    opened = 1
    for i in range(bracket_open_index+1, len(tokens)):
        token = tokens[i]
        if isinstance(token, list) and token[0] == '(':
            opened += 1
        elif isinstance(token, list) and token[0] == ')':
            opened -= 1
            if opened == 0:
                return i

    raise Exception(f'Could not find corresponding closing bracket for open bracket at index: {bracket_open_index}')

def handle_bracket(tokens):
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if isinstance(token, list) and token[0] == '(':
            # we have to first parse everything inside this
            # '(' ... ')' pair
            # to find its bracket end
            j = find_bracket_end(tokens, i)
            tokens[i:j+1] = parse(tokens[i+1:j])
            #
            i = i
        else:
            i += 1
    return tokens

def handle_division(tokens):
    # a / b / c => (a / b) / c
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if isinstance(token, list) and token[0] == '/':
            left, right = tokens[i-1], tokens[i+1]
            tokens[i-1:i+2] = [Divide(left=parse_token(left),
                                     right=parse_token(right))]
            # 3 tokens replaced by 1
            # 0 1 2 3(/) 4
            # 0 1 2=23(/)4 3
            i = i
            continue
        else:
            i += 1

    return tokens

def handle_multiplication(tokens):
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if isinstance(token, list) and token[0] == '*':
            left, right = tokens[i-1], tokens[i+1]
            tokens[i-1:i+2] = [Multiply(left=parse_token(left),
                                       right=parse_token(right))]
            i = i
            continue
        else:
            i += 1
    return tokens

def handle_addition(tokens):
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if isinstance(token, list) and token[0] == '+':
            left, right = tokens[i-1], tokens[i+1]
            tokens[i-1:i+2] = [Add(left=parse_token(left),
                                  right=parse_token(right))]
            i = i
            continue
        else:
            i += 1
    return tokens

def handle_subtraction(tokens):
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if isinstance(token, list) and token[0] == '-':
            left, right = tokens[i-1], tokens[i+1]
            tokens[i-1:i+2] = [Subtract(left=parse_token(left),
                                       right=parse_token(right))]
            i = i
            continue
        else:
            i += 1
    return tokens

def parse_token(token) -> Parsed:
    if isinstance(token, Parsed):
        return token
    # either is an operation
    # or is a number
    if token[0] == 'Number':
        return Number(value=token[1])

    # token must be an operation
    # We can't parse an operation in isolation
    raise Exception(f'Cannot process operation: {token} in isolation')

def parse(tokens):
    tokens = handle_bracket(tokens)
    tokens = handle_division(tokens)
    tokens = handle_multiplication(tokens)
    tokens = handle_addition(tokens)
    tokens = handle_subtraction(tokens)
    return tokens
