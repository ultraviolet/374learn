NUM_ELEMENTS_TO_CHECK = 30


def isInLanguage(x):
    for m in range(len(x) // 2 + 1):
        prefix = '01' * m
        if x.startswith(prefix):
            suffix = x[len(prefix):]
            if len(suffix) % 2 == 0:
                n = len(suffix) // 2
                if suffix == '10' * n and n >= m:
                    return True
    return False
