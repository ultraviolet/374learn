import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "Half L"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{w \mid ww \in L\}$$

In other words, $L'$ contains all strings $w$ such that concatenating $w$ with itself produces a string in $L$.

For example, if $w = 01$, then $ww = 0101$.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, to construct an NFA $M'$ that accepts $w$ if $ww \in L$, we need to simulate reading $ww$ on $M$. The challenge is that we don't know where the first $w$ ends and the second $w$ begins while reading the input.

The key insight is to non-deterministically guess a "hinge" state $h$ where the first $w$ ends and the second $w$ begins. We need:
1. Starting from the initial state $s$ and reading $w$, we reach state $h$
2. Starting from state $h$ and reading $w$ (the same string), we reach an accepting state

To achieve this, we use states of the form $(p, h, q)$, where:
- $p$ represents the current state when reading the first copy of $w$ starting from $s$
- $h$ is the "hinge" state where the first $w$ ends and second $w$ begins
- $q$ represents the current state when reading the second copy of $w$ starting from $h$

The construction uses an epsilon transition to non-deterministically choose the hinge state $h$. Both simulations start at the same position in the input:
- We track how far we are in the first $w$ by updating $p$ from $s$
- We track how far we are in the second $w$ by updating $q$ from $h$

After reading all of the input string:
- The first simulation should have reached the hinge state: $p = h$
- The second simulation should have reached an accepting state: $q \in A$

Therefore, accepting states are $(h, h, q)$ where $q \in A$.
"""


def should_use_dfa(M: DFA) -> bool:
    """
    This function is used to reject DFAs which aren't "interesting".

    For this problem, we consider a DFA to be interesting if it has diverse behavior on 0s and 1s
    and has at least one accepting state.
    """
    return (
        all(
            M.transitions[q]["0"] != q or M.transitions[q]["1"] != q
            for q in M.states
        )
        and len(M.final_states) > 0
    )


def construct_M_prime(M: DFA) -> NFA:
    assert M.input_symbols == {"0", "1"}

    # States are triples (p, h, q) plus a START state
    states = set(product(M.states, M.states, M.states)) | {"START"}

    transitions: NFATransitionsT = {q_prime: {"0": set(), "1": set(), "": set()} for q_prime in states}

    # Epsilon transition from START to all (s, h, h) triples
    # This non-deterministically chooses the hinge state h
    for h in M.states:
        transitions["START"][""].add((M.initial_state, h, h))

    for p in M.states:
        for h in M.states:
            for q in M.states:
                for symbol in M.input_symbols:
                    # Both simulations advance on the same symbol
                    p_next = M.transitions[p][symbol]
                    q_next = M.transitions[q][symbol]
                    transitions[(p, h, q)][symbol].add((p_next, h, q_next))

    initial_state = "START"

    # Accepting states: (h, h, q) where q is accepting in M
    # This means: first simulation reached hinge h, second simulation reached accepting state q
    final_states = {(h, h, q) for h in M.states for q in M.final_states}

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

    # Ask about transitions for a few state triples
    states_list = list(M.states)
    transitions_to_ask = [
        ((random.choice(states_list), random.choice(states_list), random.choice(states_list)), a)
        for a in M.input_symbols
        for _ in range(2)  # Ask about 2 triples per symbol
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
