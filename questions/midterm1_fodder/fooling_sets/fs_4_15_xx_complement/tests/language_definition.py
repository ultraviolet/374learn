NUM_ELEMENTS_TO_CHECK = 30


def isInLanguage(x):
    if len(x) % 2 != 0:
        return False
    n = len(x) // 2
    left, right = x[:n], x[n:]
    complement = left.translate(str.maketrans('01', '10'))
    return right == complement
