import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "DELETE0"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{w \in \Sigma^* \mid \mathit{delete0}(w) \in L\}$$

where $\mathit{delete0}(w)$ takes a string $w$ as input, and returns the string formed by removing all $0$s from $w$.

For example, $\mathit{delete0}(11000010) = 1111$.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, as $M'$ reads the input string, it needs to skip all $0$s and only feed $1$s to the simulation of $M$. The construction is straightforward because we don't need to track additional information beyond what state $M$ is in.

Every state $q$ in the DFA $M$ will correspond to exactly one state in $M'$:

- The state $q$ in $M'$ means that the simulation of $M$ is in state $q$ after processing all the $1$s seen so far (ignoring all $0$s).
"""

STATE_LABELS = ["normal"]


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

    states = M.states

    transitions: NFATransitionsT = {q: dict() for q in states}
    for q in M.states:
        # On 0: stay in the same state (skip the 0, don't feed to M)
        transitions[q]["0"] = {q}
        # On 1: feed to M (advance M's simulation)
        transitions[q]["1"] = {M.transitions[q]["1"]}

    initial_state = M.initial_state

    final_states = M.final_states

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
        (random.choice(list(M.states)), a)
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
