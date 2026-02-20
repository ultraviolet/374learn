NUM_ELEMENTS_TO_CHECK = 30


import re
def isInLanguage(x):
    m = re.fullmatch(r'(0*)(1*)(0*)', x)
    if not m:
        return False
    i, j, k = len(m.group(1)), len(m.group(2)), len(m.group(3))
    return i + j == 2 * k
