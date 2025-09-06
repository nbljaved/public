from easy_mode import Block, Col, Row

def test_lays_out_a_grid_of_rows_of_columns():
    fixture = Col(
        Row(Block(1, 2), Block(3, 4)),
        Row(Block(5, 6), Col(Block(7, 8), Block(9, 10)))
    )
    assert fixture.get_width() == 14
    assert fixture.get_height() == 22
