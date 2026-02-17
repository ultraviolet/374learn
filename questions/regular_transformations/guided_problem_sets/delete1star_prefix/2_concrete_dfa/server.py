import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "DELETE1STAR_PREFIX"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{w \mid 1^n \cdot w \in L ~\text{for some}~ n \ge 0\}.$$

In other words, $L'$ consists of all strings that can be formed by removing a (possibly empty) prefix of consecutive 1s from a string in $L$.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, as $M'$ reads the input string, it will feed the characters to a simulation of $M$. However, $M'$ will *non-deterministically* choose to insert an arbitrary number of consecutive 1s at the beginning of the simulation before reading any input. Keeping this intuition in mind, we will now make the description more formal.

Every state $q$ in the DFA $M$ will correspond to two states in $M'$, as described below:

- The state $(q, \text{inserting1s})$ means that the simulation of $M$ is in state $q$ and $M'$ is currently inserting 1s into the simulation (it may insert more, or decide to stop and start reading input).
- The state $(q, \text{after})$ means that the simulation of $M$ is in state $q$ and $M'$ has finished inserting the prefix of 1s and is now reading the input string normally.
"""

INSERTING1S = "inserting1s"
AFTER = "after"
STATE_LABELS = [INSERTING1S, AFTER]


def should_use_dfa(M: DFA) -> bool:
    """
    This function is used to reject DFAs which aren't "interesting".

    For this problem, we consider a DFA to be interesting if it has no self-loops on 1.
    This ensures students understand that 1s are being inserted at the beginning.
    When there are self-loops on 1, inserting vs. not inserting a 1 could have the same result.
    """

    return all(
        M.transitions[q]["1"] != q for q in M.states
    )


def construct_M_prime(M: DFA) -> NFA:
    assert M.input_symbols == {"0", "1"}

    states = set(product(M.states, STATE_LABELS))

    transitions: NFATransitionsT = {q_prime: dict() for q_prime in states}
    for q in M.states:
        # From inserting1s state:
        # Use epsilon to either insert another 1 or stop inserting and start reading input
        transitions[(q, INSERTING1S)][""] = {
            (M.transitions[q]["1"], INSERTING1S),  # Insert another 1
            (q, AFTER),  # Stop inserting, start reading input
        }

        # From after state:
        # Feed all characters normally
        for a in M.input_symbols:
            transitions[(q, AFTER)][a] = {(M.transitions[q][a], AFTER)}

    initial_state = (M.initial_state, INSERTING1S)

    final_states = set(product(M.final_states, {AFTER}))

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

    transitions_to_ask = [
        ((random.choice(list(M.states)), label), a)
        for label in STATE_LABELS
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
