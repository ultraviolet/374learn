import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA


TRANSFORMATION_NAME = "TAKE2SKIP2"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{\mathit{take2skip2}(w) \mid w \in L\}$$

where $\mathit{take2skip2}(w)$ takes the first two symbols of $w$, skip the next two, takes the next two, skips the next two, and so on.

For example, $\mathit{take2skip2}(010) = 01$ and $\mathit{take2skip2}(01011001) = 0101$.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, as $M'$ reads the input string, it needs to expand the string by inserting arbitrary symbols at positions 3, 4, 7, 8, 11, 12, etc. before feeding it to the simulation of $M$. When $M'$ reads symbols at positions 1-2, 5-6, 9-10, etc., it feeds those symbols to $M$. At positions 3-4, 7-8, etc., $M'$ must non-deterministically guess what symbols to feed to $M$.

Every state $q$ in the DFA $M$ will correspond to four states in $M'$, as described below:

- The state $(q, 0)$ means that the simulation of $M$ is in state $q$ and $M'$ has read 0 symbols from the current 4-symbol block (about to read the 1st symbol of the block, which will be fed to $M$).
- The state $(q, 1)$ means that the simulation of $M$ is in state $q$ and $M'$ has read 1 symbol from the current block (about to read the 2nd symbol of the block, which will be fed to $M$).
- The state $(q, 2)$ means that the simulation of $M$ is in state $q$ and $M'$ has read 2 symbols from the current block (about to read the 3rd symbol of the block, which will be skipped but $M$ still needs to advance).
- The state $(q, 3)$ means that the simulation of $M$ is in state $q$ and $M'$ has read 3 symbols from the current block (about to read the 4th symbol of the block, which will be skipped but $M$ still needs to advance).
"""

STATE_LABELS = [0, 1, 2, 3]


def should_use_dfa(M: DFA) -> bool:
    """
    This function is used to reject DFAs which aren't "interesting".

    For this problem, we consider a DFA to be interesting if it has diverse behavior on 0s and 1s.
    """
    return all(
        M.transitions[q]["0"] != q or M.transitions[q]["1"] != q
        for q in M.states
    )


def construct_M_prime(M: DFA) -> DFA:
    assert M.input_symbols == {"0", "1"}

    states = set(product(M.states, STATE_LABELS))

    transitions = {q_prime: dict() for q_prime in states}
    for q in M.states:
        # Position 0 (1st of block): feed to M, move to position 1
        transitions[(q, 0)]["0"] = (M.transitions[q]["0"], 1)
        transitions[(q, 0)]["1"] = (M.transitions[q]["1"], 1)

        # Position 1 (2nd of block): feed to M, move to position 2
        transitions[(q, 1)]["0"] = (M.transitions[q]["0"], 2)
        transitions[(q, 1)]["1"] = (M.transitions[q]["1"], 2)

        # Position 2 (3rd of block): skip, stay in same M state, move to position 3
        transitions[(q, 2)]["0"] = (q, 3)
        transitions[(q, 2)]["1"] = (q, 3)

        # Position 3 (4th of block): skip, stay in same M state, move to position 0
        transitions[(q, 3)]["0"] = (q, 0)
        transitions[(q, 3)]["1"] = (q, 0)

    initial_state = (M.initial_state, 0)

    # Accept in any state if M would accept, in any position
    final_states = set(product(M.final_states, STATE_LABELS))

    return DFA(
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
