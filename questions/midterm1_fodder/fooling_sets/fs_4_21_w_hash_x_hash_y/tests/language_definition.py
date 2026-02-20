NUM_ELEMENTS_TO_CHECK = 30


def isInLanguage(x):
    parts = x.split('#')
    if len(parts) != 3:
        return False
    w, xp, y = parts
    if not all(c in '01' for c in w + xp + y):
        return False
    return not (w == xp == y)
