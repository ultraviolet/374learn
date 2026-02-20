NUM_ELEMENTS_TO_CHECK = 15


def isInLanguage(x):
    if not x or not all(c == '0' for c in x):
        return False
    n = len(x)
    while n > 1:
        if n % 2 != 0:
            return False
        n //= 2
    return True
