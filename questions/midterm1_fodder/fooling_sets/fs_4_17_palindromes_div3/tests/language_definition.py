NUM_ELEMENTS_TO_CHECK = 30


def isInLanguage(x):
    return len(x) % 3 == 0 and x == x[::-1]
