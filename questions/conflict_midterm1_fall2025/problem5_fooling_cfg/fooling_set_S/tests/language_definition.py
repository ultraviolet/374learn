NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x):
    """Return True iff x is in (BAN+ANA)* with equal counts of BAN and ANA."""
    i = 0
    ban_count = 0
    ana_count = 0
    while i < len(x):
        if x[i:i+3] == "BAN":
            ban_count += 1
            i += 3
        elif x[i:i+3] == "ANA":
            ana_count += 1
            i += 3
        else:
            return False  # not in (BAN + ANA)*
    return ban_count == ana_count
