import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "DELETE_FIFTH"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{xy \mid xay \in L ~\text{for some}~x,y \in \Sigma^* ~\text{and}~ a \in \Sigma ~\text{such that}~ |y| = 4\}$$

In other words, $L'$ is the language obtained by taking strings from $L$ and deleting the 5th character from the end (if it exists).

For example, if $w = 1100010 \in L$, then $110010 \in L'$ (delete the 5th character from the end).
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, as $M'$ reads the input string, it needs to non-deterministically guess where to insert a character (the one that will be deleted) such that when we place it at the 5th position from the end, the resulting string is accepted by $M$. The construction tracks whether we are still reading the prefix (before the deletion point) or reading the last 4 characters (after the deletion point).

Every state $q$ in the DFA $M$ will correspond to multiple states in $M'$, as described below:

- The state $(q, \text{before})$ means that the simulation of $M$ is in state $q$ and we haven't yet non-deterministically chosen to delete a character. We are still processing the prefix.
- The state $(q, i, \text{after})$ for $i \in \{0, 1, 2, 3, 4\}$ means that the simulation of $M$ is in state $q$, we have already non-deterministically chosen the deletion point (by guessing which character to insert), and we have read exactly $i$ more characters since that guess. When $i = 4$, we know we have read exactly 4 characters after the deletion point, so the guessed character would be at the 5th position from the end.
"""

BEFORE = "before"
AFTER = "after"
STATE_LABELS = [BEFORE] + [(i, AFTER) for i in range(5)]


def should_use_dfa(M: DFA) -> bool:
    """
    This function is used to reject DFAs which aren't "interesting".

    For this problem, we consider a DFA to be interesting if it has diverse behavior on 0s and 1s.
    """
    return all(
        M.transitions[q]["0"] != q or M.transitions[q]["1"] != q
        for q in M.states
    )


def construct_M_prime(M: DFA) -> NFA:
    assert M.input_symbols == {"0", "1"}

    states = {(q, BEFORE) for q in M.states} | {
        (q, i, AFTER) for q in M.states for i in range(5)
    }

    transitions: NFATransitionsT = {q_prime: dict() for q_prime in states}
    for q in M.states:
        # From "before" state, non-deterministically choose the deletion point
        # via epsilon transition that guesses which character to insert
        transitions[(q, BEFORE)][""] = {
            (M.transitions[q][a], 0, AFTER) for a in M.input_symbols
        }

        # Also can continue reading in "before" state
        for c in M.input_symbols:
            transitions[(q, BEFORE)][c] = {(M.transitions[q][c], BEFORE)}

        # After choosing the deletion point, count the next 4 characters
        for c in M.input_symbols:
            for i in range(4):
                transitions[(q, i, AFTER)][c] = {
                    (M.transitions[q][c], i + 1, AFTER)
                }

    initial_state = (M.initial_state, BEFORE)

    # Accept if we are in an accepting state and have read exactly 4 characters after the deletion
    final_states = {(q, 4, AFTER) for q in M.final_states}

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
        ((q, BEFORE), a) for a in M.input_symbols
    ] + [
        ((q, i, AFTER), a)
        for i in range(4)           # 0-3 only; (q,4,AFTER) has no transitions
        for a in M.input_symbols
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
