NUM_ELEMENTS_TO_CHECK = 10


def isInLanguage(x):
    if not x or not all(c == '0' for c in x):
        return False
    n = len(x)
    while n > 1:
        if n % 3 != 0:
            return False
        n //= 3
    return True
