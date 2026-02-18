def generate(data):
    data["params"]["question_text"] = r"""The parity of a bit-string w is 0 if w has an even number of 1s, and 1 if w has an odd number of 1s.

Give a self-contained, formal, recursive definition of the parity function. In particular, do NOT refer to # or other functions defined in class."""

    data["params"]["rubric"] = r"""A complete answer requires all of the following (score = fraction of criteria met):
1. Base case: parity(ε) = 0
2. Recursive case for appending 0: parity(w·0) = parity(w)
3. Recursive case for appending 1: parity(w·1) = 1 - parity(w)  [equivalently: XOR 1, or (parity(w)+1) mod 2]
4. Self-contained: no reference to #0, #1, counting functions, or anything defined in class

Acceptable variants:
- Leading-character recursion: parity(0w) = parity(w), parity(1w) = 1 - parity(w)
- Single recursive case: parity(wa) = parity(w) if a=0, else 1-parity(w)
- XOR notation for case 3

Score 1.0 for all 4 criteria, 0.75 for any 3, 0.5 for any 2, 0.25 for any 1, 0.0 for none."""

    data["params"]["names_from_user"] = []
    data["params"]["names_for_user"] = []
