from .parse_arithmetic import *
from .tokenize_arithmetic import *
from pprint import pprint

def test_tokenize():
    example = '(3 + 3) / -.6 - -10 * 1.0'
    expected = [['('],
                ['Number', '3'],
                ['+'],
                ['Number', '3'],
                [')'],
                ['/'],
                ['Number', '-.6'],
                ['-'],
                ['Number', '-10'],
                ['*'],
                ['Number', '1.0']]
    actual = tokenize(example)
    assert actual == expected

def test_parse():
    example = '(3 + 3) / -.6 - -10 * 1.0'
    tokens = tokenize(example)
    actual = parse(tokens)
    expected = [Subtract(left=Divide(left=Add(left=Number(value='3'),
                                              right=Number(value='3'),
                                              op='+'),
                                     right=Number(value='-.6'),
                                     op='*'),
                         right=Multiply(left=Number(value='-10'),
                                        right=Number(value='1.0'),
                                        op='*'),
                         op='-')]
    assert actual == expected

def test_ast():
    example = '(3 + 3) / -.6 - -10 * 1.0'
    tokens = tokenize(example)
    parsed_list = parse(tokens)
    actual = parsed_list[0]()
    expected = ['-', ['*', ['+', '3', '3'], '-.6'], ['*', '-10', '1.0']]
    assert actual == expected
