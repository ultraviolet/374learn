NUM_ELEMENTS_TO_CHECK = 20


def isInLanguage(x):
    if not all(c == '0' for c in x):
        return False
    n = len(x)
    a, b = 0, 1
    while b < n:
        a, b = b, a + b
    return b == n or a == n
