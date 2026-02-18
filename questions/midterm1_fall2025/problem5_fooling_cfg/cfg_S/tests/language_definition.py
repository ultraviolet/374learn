# Language S over {i, l, n}:
# strings in (ill + ini)* with equal counts of "ill" and "ini"
# (lowercase: ill = i·l·l, ini = i·n·i)
#
# With 6 tokens max (max_length=18) we get 1+2+6+20 = 29 strings.

MAX_LEN_OVERRIDE = 18


def generateLanguage(max_length):
    """Strings in (ill+ini)* (over lowercase {i,l,n}) with #ill = #ini."""
    result = set()

    def backtrack(s, ill_count, ini_count):
        if ill_count == ini_count:
            result.add(s)
        if len(s) + 3 > max_length:
            return
        backtrack(s + "ill", ill_count + 1, ini_count)
        backtrack(s + "ini", ill_count, ini_count + 1)

    backtrack("", 0, 0)
    return result
