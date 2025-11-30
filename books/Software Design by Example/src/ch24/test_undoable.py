def test_insert_undo():
    app = make_fixture(["z", "UNDO"])
    assert get_screen(app) == ["ab", "cd"]
