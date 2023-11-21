import sys
from typing import List
from pydantic import BaseModel


class File:
    @staticmethod
    def read_file() -> List[str]:
        """Данная функция считывает текст из файла и дает на выходе list со str внутри."""
        with open("input_file.txt", "r") as file:
            data = [i for i in file.read()]
            return data

    @staticmethod
    def encoded_file(encoded_text: str):
        """Данная функция записывает закодированный текст в файл."""
        with open("file_encoded.txt", "w") as file:
            file.write(encoded_text)

    @staticmethod
    def decoded_file(decoded_text: str):
        """Данная функция записывает раскодированный текст в файл."""
        with open("file_decoded.txt", "w") as file:
            file.write(decoded_text)


class EntryText(BaseModel):
    text_to_encode: List[str] = File.read_file()


def archiver(text_encode: List[str]) -> str:
    """
    На выходе из функции получаем строку с числами. Каждое число являет собой порядковый номер закодированного символа и
    сочетания символов из словаря. Создаем изначальный словарь для записи в него unicode символов для последующего
    сжатия строки. В данном случае парой ключ - значение является символ и его номер unicode. В данном случае словарь
    гарантированно содержит знаки препинания вместе с латинскими, кириллическими символами. Если падает ошибка
    ValueError значит проблема заключается во входящем тексте. Будет выведено сообщение с проблемным символом.
    """

    # dict_all = {chr(i): i for i in range(256)} | {chr(i): i for i in range(1040, 1104)}
    dict_all = {i: ord(i) for i in text_encode}
    last_char = int(max(sorted([i for i in dict_all.values()]))) + 1
    s = ""
    res = []

    for i in text_encode:
        s_char = s + i
        try:
            if s_char in dict_all:
                s = s_char
            else:
                res.append(str(dict_all[s]))
                dict_all[s_char] = last_char
                last_char += 1
                s = i
        except KeyError:
            print(f"""Ошибка кодировки. В словаре не существует следующего символа: {s_char} """)
            break

    if s:
        res.append(str(dict_all[s]))

    encoded = ' '.join(res)
    return encoded


def unpacker(text_decode: str) -> str:
    """
    Функция распаковки на выход дает разархивированную строку.
    Обратите внимание, что словарь создается в обратном порядке. Ключом является номер unicode, а значением сам символ.
    Ошибка компрессии может выпасть при разнице в формировании словаря.
    """

    # dict_all = {**{i: chr(i) for i in range(256)}, **{i: chr(i) for i in range(1040, 1104)}}
    dict_all = {ord(i): i for i in EntryText().text_to_encode}
    last_char = int(max(sorted([i for i in dict_all.keys()]))) + 1
    inner_text = [int(i) for i in text_decode.split()]
    s = chr(inner_text.pop(0))
    res = ""
    res += s

    for i in inner_text:
        if i in dict_all:
            entry = dict_all[i]
        elif i == last_char:
            entry = s + s[0]
        else:
            raise ValueError('Ошибка в компрессии i: %s' % i)

        res += entry
        dict_all[last_char] = s + entry[0]
        last_char += 1

        s = entry
    return res


def compression_measure(encoded, res):
    """
    Данная функция делит используемый объем памяти закодированного текста на объем памяти исходного текста.
    """
    return sys.getsizeof(encoded) / sys.getsizeof(res)


if __name__ == "__main__":
    entry_text = EntryText()
    archive = archiver(entry_text.text_to_encode)
    File.encoded_file(archive)
    unpack = unpacker(archive)
    File.decoded_file(unpack)
    print("\nСтепень сжатия текста составила:", f"{1 - compression_measure(archive, entry_text.text_to_encode):.2%}")
