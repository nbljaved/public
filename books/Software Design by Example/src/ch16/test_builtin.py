from io import StringIO
from textwrap import dedent
from builtin import save

def test_save_list_flat():
    fixture = [0, False]
    expected = dedent("""\
    list:2
    int:0
    bool:False
    """)
    output = StringIO()
    save(output, fixture)
    assert output.getvalue() == expected
