import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "MOVE_1_FORWARD"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{x1yz \mid xy1z \in L\}$$

In other words, if a string in $L$ has a $1$ at some position (specifically, a string of the form $xy1z$), then the string formed by moving that $1$ one position to the right (forming $x1yz$) is in $L'$.

For example, if $0011 \in L$, then $0101 \in L'$ (the $1$ at position 2 moves to position 1).
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, as $M'$ reads the input string, it needs to "look ahead" to see if moving a $1$ forward would result in a string accepted by $M$.

The key insight is that we need to track:
1. What state $M$ would be in if we had seen the input so far
2. Whether we have "borrowed" a $1$ that we need to insert later

Every state in $M'$ has the form $(q, b)$ where:
- $q$ is a state from $M$ representing where $M$ would be after processing the transformed string so far
- $b \in \{\text{normal}, \text{borrowed}\}$ indicates whether we have borrowed a $1$ that needs to be inserted

The construction works as follows:
- **normal** states: We haven't borrowed a $1$ yet. When we see a $1$, we can either:
  - Process it normally (feed it to $M$), staying in normal mode
  - Borrow it (skip feeding it to $M$), moving to borrowed mode
- **borrowed** states: We've skipped a $1$ and need to insert it. On any input:
  - We feed a $1$ to $M$ (the borrowed one) and the current input symbol, then return to normal mode
"""

STATE_LABELS = ["normal", "borrowed"]


def should_use_dfa(M: DFA) -> bool:
    """
    This function is used to reject DFAs which aren't "interesting".

    For this problem, we want DFAs where the transformation creates interesting behavior.
    """
    # We want DFAs where 0s and 1s have different effects
    return all(
        M.transitions[q]["0"] != M.transitions[q]["1"]
        for q in M.states
    )


def construct_M_prime(M: DFA) -> NFA:
    assert M.input_symbols == {"0", "1"}

    # States: (q, label) where q is from M and label is "normal" or "borrowed"
    states = {f"({q},normal)" for q in M.states} | {f"({q},borrowed)" for q in M.states}

    transitions: NFATransitionsT = {s: dict() for s in states}

    for q in M.states:
        normal_state = f"({q},normal)"
        borrowed_state = f"({q},borrowed)"

        # From normal states:
        # On 0: just feed 0 to M, stay normal
        transitions[normal_state]["0"] = {f"({M.transitions[q]['0']},normal)"}

        # On 1: we have two choices:
        # 1. Feed the 1 normally (stay in normal mode)
        # 2. Borrow the 1 (move to borrowed mode without advancing M)
        transitions[normal_state]["1"] = {
            f"({M.transitions[q]['1']},normal)",  # process normally
            f"({q},borrowed)"  # borrow the 1
        }

        # From borrowed states (we have a 1 to insert):
        # On 0: feed "10" to M (the borrowed 1, then the 0), return to normal
        q_after_1 = M.transitions[q]["1"]
        q_after_10 = M.transitions[q_after_1]["0"]
        transitions[borrowed_state]["0"] = {f"({q_after_10},normal)"}

        # On 1: feed "11" to M (the borrowed 1, then the 1), return to normal
        q_after_11 = M.transitions[q_after_1]["1"]
        transitions[borrowed_state]["1"] = {f"({q_after_11},normal)"}

    initial_state = f"({M.initial_state},normal)"

    # A string is accepted if we end in a normal accepting state
    # (we've successfully inserted any borrowed 1)
    final_states = {f"({q},normal)" for q in M.final_states}

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
        (f"({random.choice(list(M.states))},{label})", a)
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
