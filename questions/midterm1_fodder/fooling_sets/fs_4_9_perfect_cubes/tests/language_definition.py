NUM_ELEMENTS_TO_CHECK = 20


def isInLanguage(x):
    if not all(c == '0' for c in x):
        return False
    n = len(x)
    r = round(n ** (1/3))
    for c in [r - 1, r, r + 1]:
        if c >= 0 and c ** 3 == n:
            return True
    return False
