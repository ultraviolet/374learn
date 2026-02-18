def generate(data):
    data["params"]["question_text"] = r"""L_b = {w 0^n w | w in {0,1}+, n > 0}

Prove L_b is or is not regular."""

    data["params"]["rubric"] = r"""CORRECT ANSWER: L_b is NOT regular.

KEY INSIGHT: w appears on both sides and must match exactly. Unlike part (a), the existential n does not collapse the language.

PROOF BY FOOLING SET:
  F = {1^i | i >= 1}.
  For arbitrary i != j, choose z = 0 1^i.
  - 1^i z = 1^i 0 1^i in L_b (w=1^i, n=1).
  - 1^j z = 1^j 0 1^i not in L_b (would require j=i).

--- WRONG CONCLUSION: 0/10 ---
If the student says L_b is REGULAR, score is 0 regardless of argument.

--- CORRECT CONCLUSION (NOT REGULAR): grade by proof method ---

IF FOOLING SET PROOF (standard fooling set rubric, 10 points):
  Fooling set (4 pts):
    + 2: Proposes an explicit infinite set F.
    + 2: The proposed F is actually a fooling set for L_b.
    - 0 for the proof if F is not actually a fooling set.
    - 0 for the problem if F is finite.
    - 0 for the problem if strings in F depend on more than one parameter.
  Proof (6 pts):
    Must consider arbitrary distinct x, y in F.
    - 0 for the proof unless x and y are always in F.
    - 0 for the proof unless x and y can be any pair of distinct strings in F.
    + 2: Explicitly describes a suffix z that distinguishes x and y.
    + 2: Proves xz in L_b (or yz in L_b).
    + 2: Proves yz not in L_b (or xz not in L_b, respectively).

IF CLOSURE PROPERTY PROOF (10 points):
  + 4: Identifies a regular language R and correctly argues L_b intersect R (or other operation) yields a non-regular language.
  + 6: Proves that resulting language is not regular (graded by the fooling set rubric above, scaled to 6 points).

--- ALTERNATE FOOLING SET RUBRIC (if student uses indexed form) ---
  Fooling set (4 pts):
    + 2: Proposes an infinite set X = {x_1, x_2, ...} by defining x_i for each positive integer i.
    + 2: X is actually a fooling set for L_b.
    - 0 for the proof if X is not a fooling set.
    - 0 for the problem if strings depend on more than one parameter.
  Proof (6 pts):
    Must consider arbitrary i < j.
    - 0 unless i and j can be any pair of distinct positive integers.
    + 2: Explicitly describes a suffix z_ij distinguishing x_i and x_j.
    + 2: Proves x_i z_ij in L_b (or x_j z_ij in L_b).
    + 2: Proves x_j z_ij not in L_b (or x_i z_ij not in L_b, respectively)."""

    data["params"]["names_from_user"] = []
    data["params"]["names_for_user"] = []
