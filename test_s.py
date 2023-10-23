import pytest
from LZW_algorithm.Archivator import *
from AssertionTests.test_texts import *

@pytest.mark.parametrize('text', [text_1, text_2, text_3])
def test_1(text):
    inp_text = text
    archive = archiver(inp_text)
    unpack = unpacker(archive)
    print(compression_measure(archive, unpack))
    assert text == unpack
