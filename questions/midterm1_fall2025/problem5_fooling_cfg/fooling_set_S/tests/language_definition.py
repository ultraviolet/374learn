NUM_ELEMENTS_TO_CHECK = 50


def isInLanguage(x):
    """Return True iff x is in (ILL+INI)* with equal counts of ILL and INI."""
    i = 0
    ill_count = 0
    ini_count = 0
    while i < len(x):
        if x[i:i+3] == "ILL":
            ill_count += 1
            i += 3
        elif x[i:i+3] == "INI":
            ini_count += 1
            i += 3
        else:
            return False  # not in (ILL + INI)*
    return ill_count == ini_count
