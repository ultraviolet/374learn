def generateLanguage(max_length):
    """Strings over {0,1} where the number of 0s equals twice the number of 1s."""
    result = set()
    # All such strings have length divisible by 3 (since #0 + #1 = 2*#1 + #1 = 3*#1)
    for length in range(0, max_length + 1, 3):
        ones = length // 3
        zeros = 2 * ones
        # Enumerate all binary strings of this length with exactly `zeros` 0s
        for bits in range(2**length):
            s = bin(bits)[2:].zfill(length) if length > 0 else ""
            if s.count("0") == zeros:
                result.add(s)
    return result
