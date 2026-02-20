NUM_ELEMENTS_TO_CHECK = 50


import re
def isInLanguage(x):
    runs = [len(m.group()) for m in re.finditer(r'0+', x)]
    return len(runs) >= 2 and len(set(runs)) < len(runs)
