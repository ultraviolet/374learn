NUM_ELEMENTS_TO_CHECK = 20


def isInLanguage(x: str) -> bool:
    """x ∈ L_b iff x = w·0^n·w for some w ∈ {0,1}+, n > 0."""
    n = len(x)
    for k in range(1, n):          # k = |w|
        for m in range(1, n - 2 * k + 1):  # m = number of zeros (n in the language def)
            if 2 * k + m != n:
                continue
            w = x[:k]
            zeros = x[k:k + m]
            w2 = x[k + m:]
            if all(c == '0' for c in zeros) and w == w2:
                return True
    return False
