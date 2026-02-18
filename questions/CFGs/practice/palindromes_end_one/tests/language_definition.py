from itertools import product


def generateLanguage(max_length):
    result = set()
    for length in range(max_length + 1):
        for bits in product("01", repeat=length):
            s = "".join(bits)
            if s == s[::-1] and s.endswith("1"):
                result.add(s)
    return result
