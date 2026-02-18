def generate(data):
    data["params"]["question_text"] = r"""L_a = {0^n w 0^n | w in Sigma+, n > 0}
Prove L_a is or is not regular."""
    data["params"]["rubric"] = r"""CORRECT ANSWER: L_a is REGULAR.

KEY INSIGHT: n is existentially quantified. Any 0^n w 0^n with n>0, |w|>=1 can be rewritten as 0^1 w' 0^1 where w' = 0^{n-1} w 0^{n-1} in Sigma+. So L_a = {0 w 0 | w in Sigma+} = all strings starting with 0, ending with 0, length >= 3.

VALID REGEX: 0(0|1)(0|1)*0, i.e., 0 Sigma+ 0.
VALID DFA (4 states + dead state):
  q0 (start): on 0->q1, on 1->dead
  q1 (seen opening 0): on 0->q2, on 1->q2
  q2 (len>=2, last char anything): on 0->q3, on 1->q2
  q3 (len>=3, last char 0, ACCEPT): on 0->q3, on 1->q2
  dead: on 0,1->dead

--- WRONG CONCLUSION: 0/10 ---
If the student says L_a is NOT regular, score is 0 regardless of argument.

--- CORRECT CONCLUSION (REGULAR): grade by proof method ---

IF REGEX PROOF (standard regex rubric, 10 points):
  Syntax (2 pts): Syntactically valid regular expression.
  Correctness (4 pts):
    - 4: Correct (equivalent to 0 Sigma+ 0).
    - 3: Single mistake (e.g., 0(0|1)*0 which incorrectly accepts "00").
    - 2: Incorrectly includes/excludes more than one but finitely many strings.
    - 0: Incorrectly includes/excludes infinitely many strings, or equivalent to emptyset or Sigma*.
    Every correct regex gets full credit.
  Explanation (4 pts, capped at correctness score):
    - Must explain why the regex equals L_a, not just transcribe the regex into English.

IF DFA/NFA PROOF (standard DFA rubric, 10 points):
  Syntax (2 pts): Unambiguous valid description including Q, start state, accepting states, delta.
    If transitions to a dead state are omitted, must be stated explicitly.
  Correctness (4 pts):
    - 4: Correct.
    - 3: Single mistake.
    - 2: Incorrectly accepts/rejects finitely many strings.
    - 0: Incorrectly accepts/rejects infinitely many strings, or accepts/rejects everything.
    Every correct DFA/NFA gets full credit.
  Explanation (4 pts, capped at correctness score):
    - Each state must have a mnemonic name or purpose described in English.

COMMON NEAR-MISS: 0(0|1)*0 accepts "00" which is not in L_a (need |w|>=1 so min length 3). Single-string error, 3/4 correctness."""
    data["params"]["names_from_user"] = []
    data["params"]["names_for_user"] = []