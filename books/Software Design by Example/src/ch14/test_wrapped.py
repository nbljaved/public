from wrapped import WrappedBlock, WrappedRow, WrappedCol

def test_wrap_a_row_of_two_blocks_that_do_not_fit_on_one_row():
    fixture = WrappedRow(3, WrappedBlock(2, 1), WrappedBlock(2, 1))
    wrapped = fixture.wrap()
    wrapped.place(0, 0)
    assert wrapped.report() == [
        "row",
        0, 0, 2, 2,
        [
            "col",
            0, 0, 2, 2,
            ["row", 0, 0, 2, 1, ["block", 0, 0, 2, 1]],
            ["row", 0, 1, 2, 2, ["block", 0, 1, 2, 2]],
        ],
    ]
