# Language L over {b, a, n}:
# strings in (ban + ana)* with equal counts of "ban" and "ana"
# (ban = b·a·n, ana = a·n·a)
#
# With 6 tokens max (max_length=18) we get 1+2+6+20 = 29 strings.

MAX_LEN_OVERRIDE = 18


def generateLanguage(max_length):
    """Strings in (ban+ana)* (over lowercase {b,a,n}) with #ban = #ana."""
    result = set()

    def backtrack(s, ban_count, ana_count):
        if ban_count == ana_count:
            result.add(s)
        if len(s) + 3 > max_length:
            return
        backtrack(s + "ban", ban_count + 1, ana_count)
        backtrack(s + "ana", ban_count, ana_count + 1)

    backtrack("", 0, 0)
    return result
