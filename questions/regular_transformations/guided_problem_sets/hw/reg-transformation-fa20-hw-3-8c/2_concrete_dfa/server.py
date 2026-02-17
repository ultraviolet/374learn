import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "XOR"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{z \mid z = \text{XOR}(x, y) \text{ for some } x \in L \text{ and } y \in L \text{ such that } |x| = |y|\}$$

where $\text{XOR}(x,y)$ computes the element-wise XOR of $x$ and $y$ (so for each index $i$, $z_i = x_i$ XOR $y_i$).

For example, $\text{XOR}(010, 110) = 100$.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, to construct an NFA $M'$ that accepts $z$ if $z = \text{XOR}(x, y)$ for some $x, y \in L$ with $|x| = |y|$, we need to simulate two parallel runs of $M$. As $M'$ reads each bit $z_i$ of the input string $z$, it non-deterministically guesses the corresponding bits $x_i$ and $y_i$ such that $x_i$ XOR $y_i = z_i$, and simulates $M$ on both $x$ and $y$.

The key insight is that given $z_i$, there are exactly two possibilities:
- $x_i = 0, y_i = 0$ (when $z_i = 0$)
- $x_i = 0, y_i = 1$ (when $z_i = 1$)
- $x_i = 1, y_i = 0$ (when $z_i = 1$)
- $x_i = 1, y_i = 1$ (when $z_i = 0$)

Every state in $M'$ will be a pair $(p, q)$ where $p$ and $q$ are states in $M$:
- The state $(p, q)$ means that in the first simulation, $M$ is in state $p$ (processing string $x$), and in the second simulation, $M$ is in state $q$ (processing string $y$).
"""


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

    # States are pairs (p, q) where p and q are states in M
    states = set(product(M.states, M.states))

    transitions: NFATransitionsT = {q_prime: dict() for q_prime in states}

    for p in M.states:
        for q in M.states:
            # When reading bit z:
            # - If z = 0: can have (x=0, y=0) or (x=1, y=1)
            # - If z = 1: can have (x=0, y=1) or (x=1, y=0)

            # On input 0: x=0,y=0 or x=1,y=1
            transitions[(p, q)]["0"] = {
                (M.transitions[p]["0"], M.transitions[q]["0"]),  # x=0, y=0
                (M.transitions[p]["1"], M.transitions[q]["1"])   # x=1, y=1
            }

            # On input 1: x=0,y=1 or x=1,y=0
            transitions[(p, q)]["1"] = {
                (M.transitions[p]["0"], M.transitions[q]["1"]),  # x=0, y=1
                (M.transitions[p]["1"], M.transitions[q]["0"])   # x=1, y=0
            }

    initial_state = (M.initial_state, M.initial_state)

    # Accept if both simulations end in accepting states
    final_states = set(product(M.final_states, M.final_states))

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

    # Ask about transitions for a few random state pairs
    M_states_list = list(M.states)
    transitions_to_ask = [
        ((random.choice(M_states_list), random.choice(M_states_list)), a)
        for a in M.input_symbols
        for _ in range(2)  # Ask about 2 state pairs per symbol
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
