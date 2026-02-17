import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "ThereAndBack"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{xy \mid x \in L, y^R \in L\}$$

where $w^R$ denotes the reverse of string $w$.

In other words, a string $w$ is in $L'$ if we can split it as $w = xy$ where $x \in L$ and $y^R \in L$.
"""

DESCRIPTION_OF_STATES = r"""
To construct an NFA $M'$ that accepts $L' = \{xy \mid x \in L, y^R \in L\}$, we need to recognize strings that can be split into two parts: the first part is accepted by $M$, and the reverse of the second part is also accepted by $M$.

The key insight is to use nondeterminism to guess where to split the input string:
1. First, we read the prefix $x$ using the DFA $M$ normally
2. When we nondeterministically decide we've read all of $x$, we transition to a "reversed DFA" that reads the suffix $y$ in reverse
3. We accept if we end in a state that corresponds to an accepting state of $M$ in the reversed portion

The construction works as follows:
- We create two copies of states from $M$: one copy for reading $x$ forward, and one copy for reading $y$ in reverse
- The "forward" copy operates exactly like $M$
- From any accepting state in the forward copy, we can epsilon-transition to a state in the "reverse" copy
- The "reverse" copy has all transitions reversed (like the reverse construction)
- We accept if we end at the initial state of $M$ in the reverse copy

Formally, the states in $M'$ consist of:
- States $(q, \text{fwd})$ for each state $q$ in $M$ (representing we're still reading $x$)
- States $(q, \text{rev})$ for each state $q$ in $M$ (representing we're reading $y$ backwards)

The initial state of $M'$ is $(s, \text{fwd})$ where $s$ is the initial state of $M$.

The accepting states of $M'$ are all states of the form $(s, \text{rev})$ where $s$ is the initial state of $M$ (we've successfully read a string from $M$ backwards).
"""


def should_use_dfa(M: DFA) -> bool:
    """
    This function is used to reject DFAs which aren't "interesting".

    For this problem, we consider a DFA to be interesting if it has diverse behavior
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

    # Create two copies of states: forward and reverse
    states = set()
    for q in M.states:
        states.add((q, "fwd"))
        states.add((q, "rev"))

    # Initialize transitions
    transitions: NFATransitionsT = {q: {"0": set(), "1": set(), "": set()} for q in states}

    # Forward transitions (copy of M)
    for q in M.states:
        for symbol in M.input_symbols:
            next_state = M.transitions[q][symbol]
            transitions[(q, "fwd")][symbol].add((next_state, "fwd"))

    # Epsilon transitions from accepting states in forward to reverse
    for accept_state in M.final_states:
        # We transition to the accepting state in reverse mode
        transitions[(accept_state, "fwd")][""].add((accept_state, "rev"))

    # Reverse transitions
    for q in M.states:
        for symbol in M.input_symbols:
            next_state = M.transitions[q][symbol]
            # Reverse: if q --a--> next_state in M, then next_state --a--> q in M' reverse
            transitions[(next_state, "rev")][symbol].add((q, "rev"))

    initial_state = (M.initial_state, "fwd")

    # Accept at the initial state of M in reverse mode
    final_states = {(M.initial_state, "rev")}

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

    # Ask about transitions for some states
    transitions_to_ask = [
        (random.choice([(q, mode) for q in M.states for mode in ["fwd", "rev"]]), a)
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
