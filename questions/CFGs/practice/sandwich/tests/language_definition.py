def generateLanguage(max_length):
    """Strings of the form 0^i 1^j 0^i for i >= 0, j >= 0."""
    result = set()
    for i in range(max_length // 2 + 1):
        for j in range(max_length - 2 * i + 1):
            s = "0" * i + "1" * j + "0" * i
            if len(s) <= max_length:
                result.add(s)
    return result
