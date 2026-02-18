import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "DELETE1ST"

TRANSFORMATION_DEFINITION = r"""
For any non-empty string $w$, let $\mathsf{Delete1st}(w)$ denote the string obtained by
deleting the **entire first maximal run** of identical symbols from $w$.

Given a language $L \subseteq \{0,1\}^*$, we define
$$\mathsf{DELETE1ST}(L) = \{ \mathsf{Delete1st}(w) \mid w \in L \}$$

In other words, $\mathsf{DELETE1ST}(L)$ is obtained by deleting the first maximal run of
identical symbols from every string in $L$.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, $M'$ reads the output string (after the first run has been deleted) and
simulates $M$ on the original string (before deletion). $M'$ uses $\varepsilon$-transitions
to non-deterministically consume the deleted first run, and then reads the first output
character to confirm the run was maximal and transition to the $\text{after}$ state.

Every state $q$ in the DFA $M$ will correspond to four states in $M'$, as described below:

- The state $(q, \text{start})$ means that $M$ is in state $q$ and $M'$ has not yet guessed
  which run to remove.
- The state $(q, \text{first0})$ means that $M$ is in state $q$ (having consumed some 0s
  via $\varepsilon$-transitions), and $M'$ is still guessing how long the first run of 0s was.
  Reading a 1 (the character after the first run) transitions to $\text{after}$, confirming
  the run was maximal (0s cannot follow a maximal run of 0s).
- The state $(q, \text{first1})$ means that $M$ is in state $q$ (having consumed some 1s
  via $\varepsilon$-transitions), and $M'$ is still guessing how long the first run of 1s was.
  Reading a 0 (the character after the first run) transitions to $\text{after}$, confirming
  the run was maximal.
- The state $(q, \text{after})$ means that $M$ is in state $q$, the first run has been
  fully consumed, and $M'$ is now reading the actual output string normally.
"""

START = "start"
FIRST0 = "first0"
FIRST1 = "first1"
AFTER = "after"
STATE_LABELS = [START, FIRST0, FIRST1, AFTER]


def should_use_dfa(M: DFA) -> bool:
    """Reject DFAs that aren't 'interesting'."""
    return all(
        M.transitions[q]["0"] != q or M.transitions[q]["1"] != q
        for q in M.states
    )


def construct_M_prime(M: DFA) -> NFA:
    assert M.input_symbols == {"0", "1"}

    states = set(product(M.states, STATE_LABELS))
    transitions: NFATransitionsT = {q_prime: {} for q_prime in states}

    for q in M.states:
        # (q, start): epsilon-transition to start guessing run of 0s or 1s
        transitions[(q, START)]["0"] = set()
        transitions[(q, START)]["1"] = set()
        transitions[(q, START)][""] = {
            (M.transitions[q]["0"], FIRST0),  # guess first run is 0s
            (M.transitions[q]["1"], FIRST1),  # guess first run is 1s
        }

        # (q, first0): guessing first run of 0s via epsilon-transitions
        # epsilon: continue run of 0s (can't end here — output starting with 0 would be non-maximal)
        # on 1: first run of 0s ended, start reading output (maximality: next char is 1, not 0)
        transitions[(q, FIRST0)]["0"] = set()
        transitions[(q, FIRST0)]["1"] = {(M.transitions[q]["1"], AFTER)}
        transitions[(q, FIRST0)][""] = {
            (M.transitions[q]["0"], FIRST0),  # continue run of 0s
        }

        # (q, first1): guessing first run of 1s via epsilon-transitions
        # on 0: first run of 1s ended, start reading output (maximality: next char is 0, not 1)
        transitions[(q, FIRST1)]["0"] = {(M.transitions[q]["0"], AFTER)}
        transitions[(q, FIRST1)]["1"] = set()
        transitions[(q, FIRST1)][""] = {
            (M.transitions[q]["1"], FIRST1),  # continue run of 1s
        }

        # (q, after): read actual output string normally
        transitions[(q, AFTER)]["0"] = {(M.transitions[q]["0"], AFTER)}
        transitions[(q, AFTER)]["1"] = {(M.transitions[q]["1"], AFTER)}
        transitions[(q, AFTER)][""] = set()

    initial_state = (M.initial_state, START)
    # Accept if M is in accepting state after the first run has been removed
    final_states = set(product(M.final_states, {AFTER, FIRST0, FIRST1}))

    return NFA(
        states=states,
        input_symbols=M.input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )


def generate(data: Dict[str, Any]) -> None:
    M = generate_random_dfa(3, 3)
    while not should_use_dfa(M):
        M = generate_random_dfa(3, 3)

    q = random.choice(list(M.states))
    transitions_to_ask = [
        ((q, START), ""),    # epsilon: start guessing run of 0s or 1s
        ((q, FIRST0), ""),   # epsilon: continue run of 0s
        ((q, FIRST0), "1"),  # on 1: end maximal run of 0s, go to after
        ((q, FIRST1), ""),   # epsilon: continue run of 1s
        ((q, FIRST1), "0"),  # on 0: end maximal run of 1s, go to after
        ((q, AFTER), "0"),
        ((q, AFTER), "1"),
    ]

    server_base.generate(
        data,
        TRANSFORMATION_NAME,
        TRANSFORMATION_DEFINITION,
        DESCRIPTION_OF_STATES,
        M,
        construct_M_prime(M),
        transitions_to_ask,
    )


def grade(data: pl.QuestionData) -> None:
    server_base.grade(data)
