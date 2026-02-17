import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "FLIP_SUBSTRING"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{uv^{F}w : uvw \in L ~\text{for some}~ u, v, w \in \{0, 1\}^{*}\}$$

where for a string $x \in \{0, 1\}^{*}$, $x^F$ denotes the string obtained by changing all 0's to 1's and all 1's to 0's in $x$.

For example, if $110 \in L$, then $110^F10 = 001 \in L'$ (by flipping the first two bits).
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, as $M'$ reads the input string, it will feed the characters to a simulation of $M$. However, $M'$ will *non-deterministically* choose to enter and exit a "flipping mode" where it flips the bits before feeding them to $M$. The substring processed while in flipping mode corresponds to the substring $v$ that gets flipped.

Every state $q$ in the DFA $M$ will correspond to two states in $M'$, as described below:

- The state $(q, \text{normal})$ means that the simulation of $M$ is in state $q$ and $M'$ is currently *not* flipping bits (we are in the prefix $u$ or the suffix $w$).
- The state $(q, \text{flipping})$ means that the simulation of $M$ is in state $q$ and $M'$ is currently *flipping* bits (we are in the substring $v$).
"""

NORMAL = "normal"
FLIPPING = "flipping"
STATE_LABELS = [NORMAL, FLIPPING]


def should_use_dfa(M: DFA) -> bool:
    """
    This function is used to reject DFAs which aren't "interesting".

    For this problem, we consider a DFA to be interesting if flipping bits
    actually changes behavior - i.e., the transitions on 0 and 1 are different.
    """
    return all(
        M.transitions[q]["0"] != M.transitions[q]["1"]
        for q in M.states
    )


def construct_M_prime(M: DFA) -> NFA:
    assert M.input_symbols == {"0", "1"}

    states = set(product(M.states, STATE_LABELS))

    transitions: NFATransitionsT = {q_prime: dict() for q_prime in states}
    for q in M.states:
        # In normal mode: can feed character as-is, or non-deterministically enter flipping mode
        for a in M.input_symbols:
            transitions[(q, NORMAL)][a] = {
                (M.transitions[q][a], NORMAL),  # Stay in normal mode, feed character as-is
                (M.transitions[q][str(1 - int(a))], FLIPPING)  # Enter flipping mode, flip the bit
            }

        # In flipping mode: can continue flipping, or non-deterministically exit flipping mode
        for a in M.input_symbols:
            flipped_a = str(1 - int(a))
            transitions[(q, FLIPPING)][a] = {
                (M.transitions[q][flipped_a], FLIPPING),  # Stay in flipping mode, flip the bit
                (M.transitions[q][a], NORMAL)  # Exit flipping mode, feed character as-is
            }

    initial_state = (M.initial_state, NORMAL)

    # Accept in either mode (the flipped substring v can be empty, or we could end while flipping)
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
