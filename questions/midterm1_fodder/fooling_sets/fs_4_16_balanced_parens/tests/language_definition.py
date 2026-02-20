NUM_ELEMENTS_TO_CHECK = 30


def isInLanguage(x):
    if not all(c in '()' for c in x):
        return False
    count = 0
    for c in x:
        if c == '(':
            count += 1
        else:
            count -= 1
        if count < 0:
            return False
    return count == 0
