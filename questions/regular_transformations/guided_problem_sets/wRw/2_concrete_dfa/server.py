import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "W^RW"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{w \mid w^Rw \in L\}$$

where $w^R$ denotes the reverse of string $w$.

For example, if $w = 01$, then $w^R = 10$ and $w^Rw = 1001$.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, to construct an NFA $M'$ that accepts $w$ if $w^Rw \in L$, we need to simulate two things simultaneously:
1. Reading $w$ forward on $M$
2. Reading $w$ backward on $M$ (which simulates reading $w^R$ forward)

The key insight is that the two simulations should start in the same state (where $w^R$ "passes the baton" to $w$). After reading all of $w$:
- The forward simulation should reach an accepting state of $M$
- The backward simulation should reach the initial state of $M$

To achieve this, we use states of the form $(q_i, q_j)$, where:
- $q_i$ represents the current state when reading $w$ forward on $M$
- $q_j$ represents the current state when reading $w$ backward on $M$ (simulating reading $w^R$ forward)

Since we're reading from left to right:
- For $q_i$: we can update deterministically by following forward transitions
- For $q_j$: we need to non-deterministically guess which state transitions to $q_j$ (backward simulation)

The construction uses an epsilon transition to non-deterministically choose the starting state $(q, q)$ for both simulations. After reading all of $w$:
- The forward simulation (first component) should end at an accepting state: $q_i \in A$
- The backward simulation (second component) should end at the initial state: $q_j = s$

Therefore, accepting states are $(q, s)$ where $q \in A$.
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

    # States are pairs (q_i, q_j) plus a START state
    states = set(product(M.states, M.states)) | {"START"}

    transitions: NFATransitionsT = {q_prime: {"0": set(), "1": set(), "": set()} for q_prime in states}

    # Epsilon transition from START to all (q, q) pairs
    for q in M.states:
        transitions["START"][""].add((q, q))

    for q_i in M.states:
        for q_j in M.states:
            for symbol in M.input_symbols:
                # Forward simulation (first component): q_i' = δ(q_i, a)
                q_i_next = M.transitions[q_i][symbol]

                # Backward simulation (second component): find all r such that δ(r, a) = q_j
                # Then q_j' = r
                for r in M.states:
                    if M.transitions[r][symbol] == q_j:
                        transitions[(q_i, q_j)][symbol].add((q_i_next, r))

    initial_state = "START"

    # Accepting states: (q, s) where q is accepting in M and s is initial state
    # This means: forward sim (first component) reached accepting state,
    # backward sim (second component) reached initial state
    final_states = {(q, M.initial_state) for q in M.final_states}

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

    # Ask about transitions for 2 distinct state pairs
    states_list = list(M.states)
    all_pairs = list(product(states_list, states_list))
    sampled_pairs = random.sample(all_pairs, min(2, len(all_pairs)))
    transitions_to_ask = [
        (pair, a)
        for pair in sampled_pairs
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
