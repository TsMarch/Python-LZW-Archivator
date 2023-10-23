
def archiver(text: str) -> str:
    last_char = 1104
    dict_all = {**{chr(i): i for i in range(256)}, **{chr(i): i for i in range(1040, 1104)}}

    s = ""
    res = []
    
    for i in text:
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
            raise ValueError(f"""Ошибка кодирования. В словаре не существует следующего символа: {s_char}""")
    if s:
        res.append(str(dict_all[s]))

    text = ' '.join(res)
    return text

def unpacker(text: str) -> str:
    last_char = 1104
    dict_all = {**{i: chr(i) for i in range(256)}, **{i: chr(i) for i in range(1040, 1104)}}

    text = [int(i) for i in text.split()]


    s = chr(text.pop(0))
    res = ""
    res += s

    for i in text:
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

def compression_measure(text, res):
    code_lenghth = len([int(i) for i in text.split()])
    print(code_lenghth, len(res))
    return code_lenghth/len(res)

inp = """We can't imagine our life without books. They play a very important part in our life. Books are our friends. We meet them when we are very small and can't read, but we remember our mother read them for us. We learn very much from books.
         Books educate people in different spheres of life. They develop our imagination, make us think and analyse. They help to form our character and the world outlook. Books help us in self education and in deciding problems of life. They make our life more interesting.
         People read both for knowledge and for pleasure. Different people read different books. They help us with our lessons and work. We read serious books which help us understand the life, give us answers to questions which worry us, they make us think.
         Many people enjoy so-called "easy reading" - detectives, amusing, humorous stories, fantastic. But so many people, so many tastes.
         As for me, I prefer to read adventure stories, full of interesting real fact and pictures, and detectives. My favourite author is Arthur Conan Doyle with his Holmes' adventures."""


archive = archiver(inp)
unpack = unpacker(archive)
comp = compression_measure(archive, unpack)

print(comp)