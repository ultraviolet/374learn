import random
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "DOUBLE"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{\mathit{double}(w) \mid w \in L\}$$

where $\mathit{double}(w)$ performs a left-shift operation on its input, equivalent to multiplying the binary number by 2. This operation drops the leftmost bit and appends a 0 to the right.

For example, $\mathit{double}(110100) = 101000$ and $\mathit{double}(101) = 010$.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, as $M'$ reads the input string, it needs to expand it by prepending an arbitrary symbol before feeding it to the simulation of $M$. The key insight is that $M'$ must non-deterministically guess what the first symbol of the original string was, since that symbol was dropped by the doubling operation.

The NFA $M'$ works as follows:

- $M'$ starts in the initial state of $M$, but first uses an $\varepsilon$-transition to non-deterministically transition to whichever state $M$ would reach after reading either 0 or 1. This guesses the dropped first symbol.
- For non-accepting states (other than initial), $M'$ simulates $M$ normally on the input.
- When $M$ would reach an accepting state, $M'$ must ensure the last symbol is 0 (since doubling always appends 0). So when reading a 0 at an accepting state of $M$, $M'$ transitions to a new special accept state, while also continuing to simulate $M$ in case the string continues.
"""


def should_use_dfa(M: DFA) -> bool:
    """
    This function is used to reject DFAs which aren't "interesting".

    For this problem, we consider a DFA to be interesting if it has diverse behavior.
    """
    return all(
        M.transitions[q]["0"] != q or M.transitions[q]["1"] != q
        for q in M.states
    )


def construct_M_prime(M: DFA) -> NFA:
    assert M.input_symbols == {"0", "1"}

    # Add a new accept state
    states = M.states | {"accept"}

    input_symbols = {"0", "1"}
    initial_state = M.initial_state
    final_states = {"accept"}

    transitions: NFATransitionsT = {q: {} for q in states}

    # From initial state: epsilon transition to simulate guessing the first (dropped) symbol
    # This goes to δ(s, 0) and δ(s, 1)
    transitions[M.initial_state][""] = {
        M.transitions[M.initial_state]["0"],
        M.transitions[M.initial_state]["1"]
    }

    # For non-initial, non-accepting states: simulate M normally
    for state in M.states:
        if state != M.initial_state and state not in M.final_states:
            for symbol in input_symbols:
                transitions[state][symbol] = {M.transitions[state][symbol]}

    # For accepting states: on 0, go to accept (and continue simulation)
    for state in M.final_states:
        transitions[state]["0"] = {"accept", M.transitions[state]["0"]}
        # On 1, just continue simulation (not a valid ending for doubled string)
        if "1" not in transitions[state]:
            transitions[state]["1"] = {M.transitions[state]["1"]}

    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
    )


def generate(data: Dict[str, Any]) -> None:
    M = generate_random_dfa(3, 3)
    while not should_use_dfa(M):
        M = generate_random_dfa(3, 3)

    # Ask about transitions from various states
    transitions_to_ask = []

    # Ask about epsilon transition from initial state
    transitions_to_ask.append((M.initial_state, ""))

    # Ask about regular transitions from a few states
    random_states = random.sample(list(M.states), min(2, len(M.states)))
    for state in random_states:
        if state != M.initial_state:
            for symbol in ["0", "1"]:
                transitions_to_ask.append((state, symbol))

    # Ask about transition from an accepting state on 0
    if M.final_states:
        accept_state = random.choice(list(M.final_states))
        transitions_to_ask.append((accept_state, "0"))

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
