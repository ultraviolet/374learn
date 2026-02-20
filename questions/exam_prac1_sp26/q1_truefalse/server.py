def generate(data):
    data["params"]["question_text"] = r"""For each statement below, answer "Yes" if the statement is always true and "No" otherwise, and give a brief (one short sentence) explanation of your answer.

(a) Every integer in the empty set is prime.
(b) The language {0^m 1^n | m + n ≤ 374} is regular.
(c) The language {0^m 1^n | m - n ≤ 374} is regular.
(d) For all languages L, the language L* is regular.
(e) For all languages L, the language L* is infinite.
(f) For all languages L ⊆ Σ*, if L can be represented by a regular expression, then Σ* \ L is recognized by a DFA.
(g) For all languages L and L', if L ∩ L' = ∅ and L' is not regular, then L is regular.
(h) Every regular language is recognized by a DFA with at least 374 accepting states.
(i) Every regular language is recognized by an NFA with at most 374 accepting states.
(j) Every context-free language has an infinite fooling set."""

    data["params"]["rubric"] = r"""Grade each of the 10 sub-parts (a)-(j):
- Full credit (0.1) if Yes/No is correct AND explanation is valid and clearly stated. The answer NEEDS a valid explanation or otherwise half credit must be awarded. 
- Half credit (0.05) if Yes/No is correct but explanation is missing, wrong, or unclear.
- No credit if Yes/No is wrong, or the user did not answer affirmatively or negatively.

Correct answers:
(a) Yes — vacuously true; no integers in the empty set to violate primality.
(b) Yes — finite language (bounded total length m+n ≤ 374); all finite languages are regular.
(c) No — a DFA cannot track unbounded m during the 0-reading phase, so it cannot verify m − n ≤ 374 when both m and n are large; this is not regular.
(d) No — counterexample: L = {0^n1^n | n≥0}; L* is also non-regular.
(e) No — counterexample: L = ∅, then L* = {ε}, which is finite.
(f) Yes — regular languages are closed under complement; if L is regular, Σ* \ L is regular and recognized by a DFA.
(g) No — counterexample: both L and L' can be non-regular and disjoint (e.g., L = {0^n 1^n | n≥0} and L' = {0^i 1^j | i≠j}).
(h) Yes — given any DFA for L, add unreachable accepting states to reach 374; the DFA still recognizes L.
(i) Yes — from any DFA, add ε-transitions from all accept states to a new single accept state; the resulting NFA has exactly 1 accepting state ≤ 374.
(j) No — regular languages are context-free and have FINITE fooling sets, not infinite ones."""

    data["params"]["names_from_user"] = []
    data["params"]["names_for_user"] = []
