import sys


def encoded_file(encoded_text: str):
    """Данная функция записывает закодированный текст в файл."""
    with open("file_encoded.txt", "w") as file:
        file.write(encoded_text)


def decoded_file(decoded_text: str):
    """Данная функция записывает раскодированный текст в файл."""
    with open("file_decoded.txt", "w") as file:
        file.write(decoded_text)


def read_file() -> list:
    with open("input_file.txt", "r") as file:
        data = [i for i in file.read()]
        return data


def archiver(text_encode: list) -> str:
    """
    На выходе из функции получаем строку с числами. Каждое число являет собой порядковый номер закодированного символа и
    сочетания символов из словаря. Создаем изначальный словарь для записи в него unicode символов для последующего
    сжатия строки. В данном случае парой ключ - значение является символ и его номер unicode. В данном случае словарь
    гарантированно содержит знаки препинания вместе с латинскими, кириллическими символами. Если падает ошибка
    ValueError значит проблема заключается во входящем тексте. Будет выведено сообщение с проблемным символом.
    """

    last_char = 1104
    dict_all = {**{chr(i): i for i in range(256)}, **{chr(i): i for i in range(1040, 1104)}}
    s = ""
    res = []

    for i in text_encode:
        try:
            s_char = s + i
            if s_char in dict_all:
                s = s_char
            else:
                res.append(str(dict_all[s]))
                dict_all[s_char] = last_char
                last_char += 1
                s = i
        except KeyError:
            raise ValueError(f"""Ошибка кодировки. В словаре не существует следующего символа: {s_char} """)

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

    last_char = 1104
    dict_all = {**{i: chr(i) for i in range(256)}, **{i: chr(i) for i in range(1040, 1104)}}

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
    text = read_file()
    archive = archiver(text)
    output_file = encoded_file(archive)
    unpack = unpacker(archive)
    check_file = decoded_file(unpack)
    print("\nСтепень сжатия текста составила:", f"{1 - compression_measure(archive, text):.2%}")
