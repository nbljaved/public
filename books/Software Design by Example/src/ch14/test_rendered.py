from render import render
from rendered import (RenderedBlock as Block,
                      RenderedCol as Col,
                      RenderedRow as Row,
                      )

def test_renders_a_column_of_two_blocks():
    fixture = Col(Block(1, 1), Block(2, 4))
    fixture.place(0, 0)
    expected = "\n".join(["ba", "cc", "cc", "cc", "cc"])
    assert render(fixture) == expected
