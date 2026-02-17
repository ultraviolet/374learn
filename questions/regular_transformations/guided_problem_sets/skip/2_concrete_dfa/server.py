import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "SKIP"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{\mathit{skip}(w) \mid w \in L\}$$

where $\mathit{skip}(w)$ returns the subsequence of $w$ containing only the odd-positioned symbols of $w$ (1st, 3rd, 5th, etc.).

For example, $\mathit{skip}(010101) = 000$ and $\mathit{skip}(1100) = 10$.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, as $M'$ reads the input string, it needs to expand the string by non-deterministically inserting arbitrary symbols at even positions before feeding it to the simulation of $M$. When $M'$ reads a symbol at an odd position, it feeds that symbol to $M$. At even positions, $M'$ must non-deterministically guess what symbol to feed to $M$.

Every state $q$ in the DFA $M$ will correspond to two states in $M'$, as described below:

- The state $(q, \text{odd})$ means that the simulation of $M$ is in state $q$ and $M'$ is currently at an odd position in the input (about to read a symbol that will be fed to $M$).
- The state $(q, \text{even})$ means that the simulation of $M$ is in state $q$ and $M'$ is currently at an even position in the input (about to read a symbol that won't be fed to $M$, but $M$ still needs to advance).
"""

ODD = "odd"
EVEN = "even"
STATE_LABELS = [ODD, EVEN]


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
        # From odd state (reading a symbol at odd position - this symbol stays in skip):
        # - On 0: feed 0 to M and move to even position
        transitions[(q, ODD)]["0"] = {(M.transitions[q]["0"], EVEN)}
        # - On 1: feed 1 to M and move to even position
        transitions[(q, ODD)]["1"] = {(M.transitions[q]["1"], EVEN)}

        # From even state (reading a symbol at even position - this symbol is skipped):
        # - On 0 or 1: don't feed to M (M stays in same state), move to odd position
        transitions[(q, EVEN)]["0"] = {(q, ODD)}
        transitions[(q, EVEN)]["1"] = {(q, ODD)}

    initial_state = (M.initial_state, ODD)

    final_states = set(product(M.final_states, {ODD}))

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
