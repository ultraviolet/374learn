import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "MOVEBACK8"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \text{MoveBack}_8(L) = \{xayz : xyaz \in L ~\text{for some}~ x, y, z \in \{0, 1\}^{*} ~\text{and}~ a \in \{0, 1\} ~\text{such that}~ |{y}| \leq 8\}$$

In other words, $L'$ is the language obtained by taking strings from $L$ and moving a character backward by at most 8 positions.

For example, if $w = 0100101001\textbf{1}0011 \in L$, then $01\textbf{1}001010010011 \in L'$ (move the bold $1$ backward by 8 positions).
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, as $M'$ reads the input string, it needs to non-deterministically guess where a character will be moved backward from. The construction tracks three phases: before the character is encountered, while reading the middle section (up to 8 characters that will come after the moved character), and after placing the character.

Every state $q$ in the DFA $M$ will correspond to multiple states in $M'$, as described below:

- The state $(q, \text{before})$ means that the simulation of $M$ is in state $q$ and we haven't yet non-deterministically chosen which character to move backward. We are still processing the prefix.
- The state $(q, a, i, \text{middle})$ for $a \in \{0, 1\}$ and $i \in \{0, 1, 2, 3, 4, 5, 6, 7, 8\}$ means that we have guessed that character $a$ will be moved backward, and we have read exactly $i$ characters since making that guess. These $i$ characters will appear before $a$ in the final string. When $i = 8$ or we transition via epsilon, we place character $a$ and move to the "after" phase.
- The state $(q, \text{after})$ means that the simulation of $M$ is in state $q$ and we have already placed the moved character. We continue simulating $M$ normally for the rest of the string.
"""

BEFORE = "before"
MIDDLE = "middle"
AFTER = "after"
STATE_LABELS = [BEFORE] + [(a, i, MIDDLE) for a in ["0", "1"] for i in range(9)] + [AFTER]


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

    states = (
        {(q, BEFORE) for q in M.states}
        | {
            (q, a, i, MIDDLE)
            for q in M.states
            for a in M.input_symbols
            for i in range(9)
        }
        | {(q, AFTER) for q in M.states}
    )

    transitions: NFATransitionsT = {q_prime: dict() for q_prime in states}

    for q in M.states:
        # From "before" state, we can either:
        # 1. Continue reading normally (stay in before phase)
        # 2. Non-deterministically guess this is where we pick the character to move back
        for a in M.input_symbols:
            transitions[(q, BEFORE)][a] = {
                (M.transitions[q][a], BEFORE),  # Continue in before phase
                (q, a, 0, MIDDLE),  # Start middle phase, guessing we'll move 'a' backward
            }

        # In "middle" phase with character a at position i
        for a in M.input_symbols:
            for i in range(9):
                # Read more characters (these will end up before 'a' in the result)
                if i < 8:  # Can only read up to 8 characters
                    for b in M.input_symbols:
                        transitions[(q, a, i, MIDDLE)][b] = {
                            (M.transitions[q][b], a, i + 1, MIDDLE)
                        }

                # Can transition via epsilon to place character 'a' and move to after phase
                transitions[(q, a, i, MIDDLE)][""] = {
                    (M.transitions[q][a], AFTER)
                }

        # In "after" phase, just simulate M normally
        for a in M.input_symbols:
            transitions[(q, AFTER)][a] = {(M.transitions[q][a], AFTER)}

    initial_state = (M.initial_state, BEFORE)

    # Accept if we are in an accepting state and in the "after" phase
    final_states = {(q, AFTER) for q in M.final_states}

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

    # Ask about a few representative transitions
    transitions_to_ask = [
        ((random.choice(list(M.states)), BEFORE), a)
        for a in M.input_symbols
    ] + [
        ((random.choice(list(M.states)), a, i, MIDDLE), b)
        for a in M.input_symbols
        for i in [0, 3, 7]
        for b in M.input_symbols
    ] + [
        ((random.choice(list(M.states)), AFTER), a)
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
