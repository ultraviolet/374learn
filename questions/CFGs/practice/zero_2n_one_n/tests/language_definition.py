def generateLanguage(max_length):
    """Strings of the form 0^{2n} 1^n for n >= 0."""
    result = set()
    n = 0
    while True:
        s = "0" * (2 * n) + "1" * n
        if len(s) > max_length:
            break
        result.add(s)
        n += 1
    return result
