import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA


TRANSFORMATION_NAME = "INSERT_FIFTH"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{xay \mid xy \in L ~\text{for some}~ x,y \in \Sigma^* ~\text{and}~ a \in \Sigma ~\text{such that}~ |x| = 4\}$$

In other words, $L'$ contains all strings formed by inserting any character after exactly 4 characters from a string in $L$.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, as $M'$ reads the input string, it will feed the characters to a simulation of $M$. However, $M'$ must track how many characters it has read, and when it reaches the 5th position (after reading 4 characters), it will *non-deterministically* choose a single character to omit from the simulation. Keeping this intuition in mind, we will now make the description more formal.

Every state $q$ in the DFA $M$ will correspond to six states in $M'$, as described below:

- The state $(q, i, \text{before})$ for $i \in \{0,1,2,3,4\}$ means that the simulation of $M$ is in state $q$, $M'$ has read $i$ characters so far, and $M'$ has not yet omitted the inserted character.
- The state $(q, \text{after})$ means that the simulation of $M$ is in state $q$ and $M'$ has already omitted the inserted character (which was at position 5).
"""

BEFORE = "before"
AFTER = "after"


def should_use_dfa(M: DFA) -> bool:
    """
    This function is used to reject DFAs which aren't "interesting".

    For this problem, we consider a DFA to be interesting if it has no self-loops.
    This ensures students understand that characters are being omitted from the simulation of M.
    When there are self-loops, simulating vs. not simulating a character could have the same result.
    """

    return all(
        M.transitions[q][a] != q for (q, a) in product(M.states, M.input_symbols)
    )


def construct_M_prime(M: DFA) -> DFA:
    assert M.input_symbols == {"0", "1"}

    states = {(q, i, BEFORE) for q in M.states for i in range(5)} | {
        (q, AFTER) for q in M.states
    }

    transitions = {q_prime: {} for q_prime in states}

    for q in M.states:
        for a in M.input_symbols:
            # For positions 0-3: keep counting and feed character to M
            for i in range(4):
                transitions[(q, i, BEFORE)][a] = (M.transitions[q][a], i + 1, BEFORE)

            # At position 4 (after reading 4 characters): non-deterministically choose to omit this character
            # Since we're building a DFA for the concrete example, we need to handle this differently
            # For the NFA, this would split into two paths. For DFA in teaching context,
            # we transition to the "after" state without feeding to M
            transitions[(q, 4, BEFORE)][a] = (q, AFTER)

            # After omitting: feed all characters to M
            transitions[(q, AFTER)][a] = (M.transitions[q][a], AFTER)

    initial_state = (M.initial_state, 0, BEFORE)

    final_states = {(q, AFTER) for q in M.final_states}

    return DFA(
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

    # Select representative transitions to ask about
    transitions_to_ask = [
        ((random.choice(list(M.states)), i, BEFORE), a)
        for i in [0, 2, 4]  # Ask about beginning, middle, and insertion point
        for a in M.input_symbols
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
        transitions_to_ask[:6],  # Limit to 6 transitions to keep it manageable
    )


def grade(data: pl.QuestionData) -> None:
    server_base.grade(data)
