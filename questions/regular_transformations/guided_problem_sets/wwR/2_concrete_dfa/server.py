import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "WW^R"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{w \mid ww^R \in L\}$$

where $w^R$ denotes the reverse of string $w$.

For example, if $w = 01$, then $w^R = 10$ and $ww^R = 0110$.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, to construct an NFA $M'$ that accepts $w$ if $ww^R \in L$, we need to simulate reading $w$ on $M$ and simultaneously simulate reading $w^R$ on the reversed machine $\mathit{reverse}(M)$.

The key insight is that we read $w$ from left to right, but $w^R$ is the reverse of $w$. So we need to:
1. Simulate $M$ reading $w$ forward (from left to right)
2. Simultaneously simulate $\mathit{reverse}(M)$ reading $w^R$ forward, which is equivalent to simulating $M$ reading $w$ backward (from right to left)

To achieve this, we use states of the form $(q_i, q_j)$, where:
- $q_i$ represents the current state when reading $w$ forward on $M$
- $q_j$ represents the current state when reading $w$ backward on $M$ (which simulates reading $w^R$ forward on $\mathit{reverse}(M)$)

Since we're reading from left to right, we can update $q_i$ deterministically. But for $q_j$, we need to non-deterministically guess which state to transition to because we're effectively reading backward.

After reading all of $w$, the two simulations should meet at the same state (where $w$ "passes the baton" to $w^R$). This means we accept when $q_i = q_j$ and the concatenated string $ww^R$ ends in an accepting state of $M$.

The construction:
- States: $(q_i, q_j)$ for all $q_i, q_j \in Q$
- Initial state: $(s, q)$ for any $q \in Q$ (non-deterministic choice of where the backward simulation starts)
- On reading symbol $a$:
  - Update $q_i$ by following the forward transition: $q_i' = \delta(q_i, a)$
  - Update $q_j$ by guessing which state $p$ has a transition to $q_j$ on $a$: $\delta(p, a) = q_j$, so $q_j' = p$
- Accepting states: $(q, q)$ where $q \in A$ (both simulations meet at the same accepting state)
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

    # States are pairs (q_i, q_j)
    states = set(product(M.states, M.states))

    transitions: NFATransitionsT = {q_prime: {"0": set(), "1": set(), "": set()} for q_prime in states}

    for q_i in M.states:
        for q_j in M.states:
            for symbol in M.input_symbols:
                # Forward simulation: q_i' = δ(q_i, a)
                q_i_next = M.transitions[q_i][symbol]

                # Backward simulation: find all p such that δ(p, a) = q_j
                # Then q_j' = p
                for p in M.states:
                    if M.transitions[p][symbol] == q_j:
                        transitions[(q_i, q_j)][symbol].add((q_i_next, p))

    # Initial states: (s, q) for all q in Q (non-deterministically guess starting point for backward sim)
    # We represent this with epsilon transitions from a new initial state
    new_initial = ("init", "init")
    states.add(new_initial)
    transitions[new_initial] = {"0": set(), "1": set(), "": set()}

    for q in M.states:
        transitions[new_initial][""].add((M.initial_state, q))

    initial_state = new_initial

    # Accepting states: (q, q) where q is accepting in M
    final_states = {(q, q) for q in M.final_states}

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
