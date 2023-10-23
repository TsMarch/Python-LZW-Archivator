import pytest
from LZW_algorithm.Archivator import *
from LZW_algorithm.test_texts import *

# Используем фикстуру параметризации pytest для запуска множества тестов.  
# Тест будет считаться успешно пройденным в том случае, если сжатая строка будет равна строке после распаковки.

@pytest.mark.parametrize('text', [text_1, text_2, text_3, text_4, text_5])
def test_encoder_decoder(text):
    inp_text = text
    archive = archiver(inp_text)
    unpack = unpacker(archive)
    assert text == unpack
