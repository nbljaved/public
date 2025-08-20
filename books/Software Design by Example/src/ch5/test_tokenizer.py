from .tokenizer import *

def test_tok_empty_string():
    assert Tokenizer().tok("") == []

def test_tok_any_either():
    assert Tokenizer().tok("*{abc,def}") == [
        ["Any"],
        ["EitherStart"],
        ["Lit", "abc"],
        ["Lit", "def"],
        ["EitherEnd"],
    ]
