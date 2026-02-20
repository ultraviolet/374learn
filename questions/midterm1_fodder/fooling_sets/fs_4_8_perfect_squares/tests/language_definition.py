NUM_ELEMENTS_TO_CHECK = 30


import math
def isInLanguage(x):
    if not all(c == '0' for c in x):
        return False
    n = len(x)
    r = int(math.isqrt(n))
    return r * r == n
