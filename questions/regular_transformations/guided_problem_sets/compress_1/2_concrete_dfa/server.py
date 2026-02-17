import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "COMPRESS"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{w \in \Sigma^* \mid \mathit{compress}(w) \in L\}$$

where $\mathit{compress}(w)$ takes a string $w$ as input, and returns the string formed by compressing every run of $0$s in $w$ by half. Specifically, every run of $2n$ $0$s is compressed to length $n$, and every run of $2n + 1$ $0$s is compressed to length $n + 1$.

For example, $\mathit{compress}(11000010) = 110010$.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, as $M'$ reads the input string, it needs to compress runs of $0$s before feeding them to the simulation of $M$. When $M'$ encounters a $0$, it can non-deterministically choose whether this $0$ (along with a following $0$ if present) will compress to a single $0$, or if it's a standalone $0$ that stays as-is.

Every state $q$ in the DFA $M$ will correspond to two states in $M'$, as described below:

- The state $(q, \text{normal})$ means that the simulation of $M$ is in state $q$ and $M'$ is not currently in the middle of processing a compressed pair.
- The state $(q, \text{waiting})$ means that $M'$ just read a $0$ that is the first of a pair that will compress to a single $0$, and it's waiting for the second $0$.
"""

NORMAL = "normal"
WAITING = "waiting"
STATE_LABELS = [NORMAL, WAITING]


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
        # From normal state:
        # - On 0: can stay as single 0 (feed to M), or start a compressed pair (go to waiting)
        transitions[(q, NORMAL)]["0"] = {
            (M.transitions[q]["0"], NORMAL),  # Single 0 stays
            (q, WAITING)  # Start of compressed pair
        }
        # - On 1: always feed to M (1s don't compress)
        transitions[(q, NORMAL)]["1"] = {(M.transitions[q]["1"], NORMAL)}

        # From waiting state:
        # - On 0: complete the pair, feed single 0 to M, go back to normal
        transitions[(q, WAITING)]["0"] = {(M.transitions[q]["0"], NORMAL)}
        # - On 1: not allowed (we're waiting for the second 0)
        transitions[(q, WAITING)]["1"] = set()

    initial_state = (M.initial_state, NORMAL)

    final_states = set(product(M.final_states, {NORMAL}))

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
