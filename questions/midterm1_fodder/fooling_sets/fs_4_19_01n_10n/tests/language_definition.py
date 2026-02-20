NUM_ELEMENTS_TO_CHECK = 30


def isInLanguage(x):
    if len(x) % 4 != 0:
        return len(x) == 0
    k = len(x) // 4
    return x == '01' * k + '10' * k
