from placed import (PlacedBlock as Block,
                    PlacedCol as Col,
                    PlacedRow as Row,
                    )

def test_places_a_column_of_two_blocks():
    fixture = Col(Block(1, 1), Block(2, 4))
    fixture.place(0, 0)
    assert fixture.report() == [
        "col",
        0, 0, 2, 5,
        ["block", 0, 0, 1, 1],
        ["block", 0, 1, 2, 5],
    ]
