import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "COMPRESS2"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{\mathit{compress}(w) \mid w \in L\}$$

where $\mathit{compress}(w)$ takes a string $w$ as input, and returns the string formed by compressing every run of $0$s in $w$ by half. Specifically, every run of $2n$ $0$s is compressed to length $n$, and every run of $2n + 1$ $0$s is compressed to length $n + 1$.

For example, $\mathit{compress}(11000010) = 110010$.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, as $M'$ reads the input string, it simulates $M$ by feeding characters to it, but each $0$ in the input might represent either one or two $0$s in the original string (before compression). When $M'$ encounters a $0$ in the input, it can non-deterministically choose whether to feed one $0$ or two $0$s to the simulation of $M$.

Every state $q$ in the DFA $M$ will correspond to two states in $M'$, as described below:

- The state $(q, \text{normal})$ means that the simulation of $M$ is in state $q$ and $M'$ is not currently in the middle of expanding a compressed $0$.
- The state $(q, \text{expanding})$ means that $M'$ just read a $0$ that represents two $0$s, and it has fed the first $0$ to $M$. Now $M$ is in state $q$ and $M'$ needs to feed the second $0$.
"""

NORMAL = "normal"
EXPANDING = "expanding"
STATE_LABELS = [NORMAL, EXPANDING]


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
        # - On 0: can represent single 0 (feed to M) or first of two 0s (go to expanding)
        transitions[(q, NORMAL)]["0"] = {
            (M.transitions[q]["0"], NORMAL),  # Single 0
            (M.transitions[q]["0"], EXPANDING)  # First of two 0s
        }
        # - On 1: always feed to M (1s don't compress)
        transitions[(q, NORMAL)]["1"] = {(M.transitions[q]["1"], NORMAL)}

        # From expanding state:
        # - We must feed the second 0 to M, then return to normal
        # - This happens automatically (epsilon-like), but we trigger it on the next symbol
        # - Actually, we need to feed the second 0 immediately and go back to normal
        # - We can't do epsilon transitions easily, so we handle it differently:
        # - On 0: feed the pending second 0, then process this new 0
        transitions[(q, EXPANDING)]["0"] = {
            (M.transitions[q]["0"], NORMAL),  # Feed second 0, then this 0 as single
            (M.transitions[q]["0"], EXPANDING)  # Feed second 0, then this 0 as first of pair
        }
        # - On 1: feed the pending second 0, then process this 1
        transitions[(q, EXPANDING)]["1"] = {(M.transitions[q]["1"], NORMAL)}

    initial_state = (M.initial_state, NORMAL)

    final_states = set(product(M.final_states, {NORMAL, EXPANDING}))

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
