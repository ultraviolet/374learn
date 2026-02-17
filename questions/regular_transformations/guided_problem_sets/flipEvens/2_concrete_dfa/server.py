import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "FLIPEVENS"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{\mathit{flipEvens}(w) \mid w \in L\}$$

where $\mathit{flipEvens}(w)$ inverts every even-indexed bit in $w$. For example, $\mathit{flipEvens}(01100) = 00110$.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, as $M'$ reads the input string, it will simulate $M$ while keeping track of the current position (odd or even, using 1-based indexing). When reading a character at an even position (positions 2, 4, 6, ...), $M'$ must flip it before feeding it to $M$.

Every state $q$ in the DFA $M$ will correspond to two states in $M'$, as described below:

- The state $(q, \text{odd})$ means that the simulation of $M$ is in state $q$ and we are currently at an odd position (1, 3, 5, ...).
- The state $(q, \text{even})$ means that the simulation of $M$ is in state $q$ and we are currently at an even position (2, 4, 6, ...).

Starting at position 1 (which is odd), the NFA $M'$ does NOT flip the first character. On each transition, the parity alternates between odd and even.
"""

ODD = "odd"
EVEN = "even"
STATE_LABELS = [EVEN, ODD]


def should_use_dfa(M: DFA) -> bool:
    """
    This function is used to reject DFAs which aren't "interesting".

    For this problem, we want DFAs where flipping bits matters.
    We ensure that 0 and 1 transitions are different for at least some states.
    """
    return all(
        M.transitions[q]["0"] != M.transitions[q]["1"]
        for q in M.states
    )


def flip_bit(bit: str) -> str:
    """Flip a bit: 0 -> 1, 1 -> 0"""
    return "1" if bit == "0" else "0"


def construct_M_prime(M: DFA) -> NFA:
    assert M.input_symbols == {"0", "1"}

    states = set(product(M.states, STATE_LABELS))

    transitions: NFATransitionsT = {q_prime: dict() for q_prime in states}
    for q in M.states:
        # From odd state (odd position: 1, 3, 5, ...):
        # We do NOT flip the bit, feed directly to M, then move to even
        for a in M.input_symbols:
            transitions[(q, ODD)][a] = {(M.transitions[q][a], EVEN)}

        # From even state (even position: 2, 4, 6, ...):
        # We must flip the bit before feeding to M, then move to odd
        for a in M.input_symbols:
            flipped = flip_bit(a)
            transitions[(q, EVEN)][a] = {(M.transitions[q][flipped], ODD)}

    # Start at position 1 (which is odd in 1-based indexing)
    initial_state = (M.initial_state, ODD)

    # Accept if M would accept, regardless of whether we end on odd or even position
    # Both odd and even length strings are valid
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
