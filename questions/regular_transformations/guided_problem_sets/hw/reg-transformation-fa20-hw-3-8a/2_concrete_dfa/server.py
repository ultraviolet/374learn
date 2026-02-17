import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "DELONES"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{0^{\#_0(w)} \mid w \in L\}$$

This transformation removes all $1$s from strings of $L$, keeping only the $0$s.

For example, if $w = 11000010 \in L$, then $0000 \in L'$ (all $1$s removed, leaving 4 $0$s).
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, as $M'$ reads the input string, it needs to skip all $1$s and only feed $0$s to the simulation of $M$. The construction is straightforward because we don't need to track additional information beyond what state $M$ is in.

Every state $q$ in the DFA $M$ will correspond to exactly one state in $M'$:

- The state $q$ in $M'$ means that the simulation of $M$ is in state $q$ after processing all the $0$s seen so far (ignoring all $1$s).
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
        # On 0: feed to M (advance M's simulation)
        transitions[q]["0"] = {M.transitions[q]["0"]}
        # On 1: stay in the same state (skip the 1, don't feed to M)
        transitions[q]["1"] = {q}

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
