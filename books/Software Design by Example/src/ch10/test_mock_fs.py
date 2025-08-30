import pyfakefs
from pathlib import Path

# Here 'fs' is a pytest fixture
def test_simple_example(fs):
    sentence = "this file contains one sentence."
    with open('alpha.txt', 'w') as writer:
        writer.write(sentence)
    assert Path('alpha.txt').exists()
    with open('alpha.txt', 'r') as reader:
        assert reader.read() == sentence
