def generateLanguage(max_length):
    """Strings of the form 0^i 1^j where 0 <= i <= j."""
    result = set()
    for i in range(max_length + 1):
        for j in range(i, max_length + 1):
            s = "0" * i + "1" * j
            if len(s) <= max_length:
                result.add(s)
    return result
