def generateLanguage(max_length):
    result = set()
    for n in range(max_length // 2 + 1):
        s = "0" * n + "1" * n
        if len(s) <= max_length:
            result.add(s)
    return result
