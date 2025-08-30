import pyfakefs
import pytest
from unittest.mock import patch
from backup import backup
from pathlib import Path

FILES = {"a.txt": "aaa", "b.txt": "bbb", "sub_dir/c.txt": "ccc"}

@pytest.fixture
def our_fs(fs):
    for name, contents in FILES.items():
        fs.create_file(name, contents=contents)

"""
Example of a single test (num-num power)
"""

def test_nested_example(our_fs):
    timestamp = 1234
    with patch("backup.current_time", return_value=timestamp):
        manifest = backup(".", "/backup")
    assert Path("/backup", f"{timestamp}.csv").exists()
    for filename, hash_code in manifest:
        assert Path("/backup", f"{hash_code}.bck").exists()
