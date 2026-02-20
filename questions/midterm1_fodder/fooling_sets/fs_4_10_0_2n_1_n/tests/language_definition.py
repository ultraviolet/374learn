NUM_ELEMENTS_TO_CHECK = 50


import re
def isInLanguage(x):
    m = re.fullmatch(r'(0*)(1*)', x)
    if not m:
        return False
    zeros, ones = len(m.group(1)), len(m.group(2))
    return zeros == 2 * ones
