import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "TAKE2SKIP2"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{\mathit{take2skip2}(w) \mid w \in L\}$$

where $\mathit{take2skip2}(w)$ takes the first two symbols of $w$, skips the next two, takes the next two, skips the next two, and so on.

For example, $\mathit{take2skip2}(01011011) = 0111$ and $\mathit{take2skip2}(0101) = 01$.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, as $M'$ reads the input string, it needs to expand the string by non-deterministically inserting arbitrary symbols at positions 3-4, 7-8, 11-12, etc. before feeding it to the simulation of $M$. When $M'$ reads symbols at positions 1-2, 5-6, 9-10, etc., it feeds those symbols to $M$. At positions 3-4, 7-8, 11-12, etc., $M'$ must non-deterministically guess what symbols to feed to $M$.

Every state $q$ in the DFA $M$ will correspond to four states in $M'$, as described below:

- The state $(q, \text{take1})$ means that the simulation of $M$ is in state $q$ and $M'$ is at position 1, 5, 9, ... in the input (first symbol of a "take" pair).
- The state $(q, \text{take2})$ means that the simulation of $M$ is in state $q$ and $M'$ is at position 2, 6, 10, ... in the input (second symbol of a "take" pair).
- The state $(q, \text{skip1})$ means that the simulation of $M$ is in state $q$ and $M'$ is at position 3, 7, 11, ... in the input (first symbol of a "skip" pair).
- The state $(q, \text{skip2})$ means that the simulation of $M$ is in state $q$ and $M'$ is at position 4, 8, 12, ... in the input (second symbol of a "skip" pair).
"""

TAKE1 = "take1"
TAKE2 = "take2"
SKIP1 = "skip1"
SKIP2 = "skip2"
STATE_LABELS = [TAKE1, TAKE2, SKIP1, SKIP2]


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

    states = set(product(M.states, STATE_LABELS))

    transitions: NFATransitionsT = {q_prime: dict() for q_prime in states}
    for q in M.states:
        # From take1 state (reading first symbol of "take" pair - this symbol stays):
        # - On 0: feed 0 to M and move to take2
        transitions[(q, TAKE1)]["0"] = {(M.transitions[q]["0"], TAKE2)}
        # - On 1: feed 1 to M and move to take2
        transitions[(q, TAKE1)]["1"] = {(M.transitions[q]["1"], TAKE2)}

        # From take2 state (reading second symbol of "take" pair - this symbol stays):
        # - On 0: feed 0 to M and move to skip1
        transitions[(q, TAKE2)]["0"] = {(M.transitions[q]["0"], SKIP1)}
        # - On 1: feed 1 to M and move to skip1
        transitions[(q, TAKE2)]["1"] = {(M.transitions[q]["1"], SKIP1)}

        # From skip1 state (reading first symbol of "skip" pair - this symbol is skipped):
        # - On 0 or 1: don't feed to M (M stays in same state), move to skip2
        transitions[(q, SKIP1)]["0"] = {(q, SKIP2)}
        transitions[(q, SKIP1)]["1"] = {(q, SKIP2)}

        # From skip2 state (reading second symbol of "skip" pair - this symbol is skipped):
        # - On 0 or 1: don't feed to M (M stays in same state), move to take1
        transitions[(q, SKIP2)]["0"] = {(q, TAKE1)}
        transitions[(q, SKIP2)]["1"] = {(q, TAKE1)}

    initial_state = (M.initial_state, TAKE1)

    # Accept if we're in an accepting state of M and we're in take1, take2, skip1, or skip2
    # (we can end after any position in the cycle)
    final_states = set(product(M.final_states, STATE_LABELS))

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
