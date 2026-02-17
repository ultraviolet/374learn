import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "THIRDS"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{\mathit{thirds}(w) \mid w \in L\}$$

where $\mathit{thirds}(w)$ returns the subsequence of $w$ containing every third symbol (positions 3, 6, 9, etc.).

For example, $\mathit{thirds}(011000110) = 100$ and $\mathit{thirds}(01101) = 1$.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, as $M'$ reads the input string, it needs to expand the string by non-deterministically inserting arbitrary symbols at positions that are not multiples of 3 before feeding it to the simulation of $M$. When $M'$ reads a symbol at a position that is a multiple of 3, it feeds that symbol to $M$. At other positions, $M'$ must non-deterministically guess what symbols to insert.

Every state $q$ in the DFA $M$ will correspond to three states in $M'$, as described below:

- The state $(q, 0)$ means that the simulation of $M$ is in state $q$ and $M'$ has just read a symbol at a position that is a multiple of 3 (positions 3, 6, 9, ...). This symbol was fed to $M$.
- The state $(q, 1)$ means that the simulation of $M$ is in state $q$ and $M'$ is at position $\equiv 1 \pmod{3}$ (positions 1, 4, 7, ...). The next symbol will not be fed to $M$.
- The state $(q, 2)$ means that the simulation of $M$ is in state $q$ and $M'$ is at position $\equiv 2 \pmod{3}$ (positions 2, 5, 8, ...). The next symbol will not be fed to $M$ yet.
"""

POS_0 = 0  # Just read position 3, 6, 9, ... (multiple of 3, fed to M)
POS_1 = 1  # At position 1, 4, 7, ... (≡ 1 mod 3)
POS_2 = 2  # At position 2, 5, 8, ... (≡ 2 mod 3)
STATE_LABELS = [POS_0, POS_1, POS_2]


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
        # From position 0 (just read a multiple of 3):
        # - On 0 or 1: don't feed to M, move to position 1
        transitions[(q, POS_0)]["0"] = {(q, POS_1)}
        transitions[(q, POS_0)]["1"] = {(q, POS_1)}

        # From position 1 (at position ≡ 1 mod 3):
        # - On 0 or 1: don't feed to M, move to position 2
        transitions[(q, POS_1)]["0"] = {(q, POS_2)}
        transitions[(q, POS_1)]["1"] = {(q, POS_2)}

        # From position 2 (at position ≡ 2 mod 3):
        # - On 0: feed 0 to M and move to position 0
        transitions[(q, POS_2)]["0"] = {(M.transitions[q]["0"], POS_0)}
        # - On 1: feed 1 to M and move to position 0
        transitions[(q, POS_2)]["1"] = {(M.transitions[q]["1"], POS_0)}

    initial_state = (M.initial_state, POS_1)

    # Accept only in states where M accepts and we're at position 0 (just completed a cycle)
    final_states = set(product(M.final_states, {POS_0}))

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
