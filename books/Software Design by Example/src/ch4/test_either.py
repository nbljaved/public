from matcher import *

def test_either_two_literals_first():
    # /{a,b,c}/ matches "a"
    assert Either(Lit("a"), Lit("b")).match("a")

def test_either_two_literals_not_both():
    # /{a,b,c}/ doesn't match "ab"
    assert not Either(Lit("a"), Lit("b"), Lit("c")).match("ab")

def test_either_followed_by_literal_match():
    # /{a,b,c}d/ matches "cd"
    assert Either(Lit("a"), Lit("b"), Lit("c"), rest=Lit("d")).match("cd")

def test_either_followed_by_literal_no_match():
    # /{a,b,c}d/ doesn't match "cx"
    assert not Either(Lit("a"), Lit("b"), Lit("c"), rest=Lit("d")).match("cx")

def test_either_followed_by_literal_no_match2():
    # /{a,b,cd}d/ matches "cd"
    assert not Either(Lit("a"), Lit("b"), Lit("cd"), rest=Lit("d")).match("cd")

def test_empty_either_empty_literal_match():
    # /{}/ matches ""
    assert Either().match("")

def test_empty_either_literal_match():
    # /{}abc/ matches ""
    assert Either(rest=Lit("abc")).match("abc")

def test_empty_either_literal_no_match():
    # /{}abc/ doesn't match "abd"
    assert not Either().match("abd")
