NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x):
    parts = x.split('#')
    if len(parts) != 2:
        return False
    left, right = parts
    if not all(c in '01' for c in left + right):
        return False
    return left.count('0') == right.count('1')
