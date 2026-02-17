import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "REVERSE"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{w \in \Sigma^* \mid w^R \in L\}$$

where $w^R$ denotes the reverse of string $w$.

For example, if $w = 0110$, then $w^R = 0110$.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, to construct an NFA $M'$ that accepts $w$ if $w^R \in L$, we reverse the operation of the DFA $M$. The key insight is that reading $w$ forward in $M'$ should be equivalent to reading $w^R$ forward in $M$, which is the same as reading $w$ backward in $M$.

The construction reverses all transitions:
- A transition from state $p$ to state $q$ on symbol $a$ in $M$ becomes a transition from state $q$ to state $p$ on symbol $a$ in $M'$
- The initial state of $M$ becomes the only accepting state of $M'$
- The accepting states of $M$ become the initial states of $M'$ (we need a new single initial state that epsilon-transitions to all of them)

Since we need a single initial state, we introduce a new state $s'$ that has epsilon transitions to all states that were accepting in $M$.

Every state $q$ in the DFA $M$ will correspond to a state in $M'$, plus we add one new initial state.
"""


def should_use_dfa(M: DFA) -> bool:
    """
    This function is used to reject DFAs which aren't "interesting".

    For this problem, we consider a DFA to be interesting if it has diverse behavior on 0s and 1s
    and has at least one accepting state that isn't the initial state.
    """
    return (
        all(
            M.transitions[q]["0"] != q or M.transitions[q]["1"] != q
            for q in M.states
        )
        and len(M.final_states) > 0
        and not (len(M.final_states) == 1 and M.initial_state in M.final_states)
    )


def construct_M_prime(M: DFA) -> NFA:
    assert M.input_symbols == {"0", "1"}

    # Add a new initial state
    new_initial = "s'"
    states = M.states | {new_initial}

    # Reverse all transitions
    transitions: NFATransitionsT = {q: {"0": set(), "1": set(), "": set()} for q in states}

    for q in M.states:
        for symbol in M.input_symbols:
            next_state = M.transitions[q][symbol]
            # Reverse: if q --a--> next_state in M, then next_state --a--> q in M'
            transitions[next_state][symbol].add(q)

    # Add epsilon transitions from new initial state to all former accepting states
    for accept_state in M.final_states:
        transitions[new_initial][""].add(accept_state)

    initial_state = new_initial

    # The only accepting state is the former initial state
    final_states = {M.initial_state}

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

    # Ask about transitions for each state and each input symbol
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
