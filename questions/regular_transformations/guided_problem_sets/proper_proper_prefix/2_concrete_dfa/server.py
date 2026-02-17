import random
from typing import Any, Dict, Set

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA


TRANSFORMATION_NAME = "PPPREFIX"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$\mathsf{PPPREFIX}(L) = \{x \mid x \text{ is a proper-proper prefix of some string } w \in L\}.$$

Or alternatively,
$$\mathsf{PPPREFIX}(L) = \{ x \mid xy \in L ~\text{for some}~ y\in\Sigma^* ~\text{such that}~ |y|\ge 2 \}.$$

Given a string $w$, a prefix is any string $x$ such that there is a string $y$ such
that $xy=w$. A proper prefix of $w$ is a string $x$ such that there is a $y$ with
$|y| \geq 1$ such that $xy=w$. We will call a string $x$ a proper-proper prefix
of $w$ if there is a string y such that $|y| \geq 2$ and $xy = w$.

For example, if $w = abcde$, then $abc, ab, a,$ and $\epsilon$ are proper-proper prefixes of $w$.
"""

DESCRIPTION_OF_STATES = r"""
This transformation modifies only the accepting states of the DFA. The key insight is that a state $q$ should be accepting in $M'$ if and only if there exists a path of length 2 or more from $q$ to some accepting state in $M$.

In other words, $M'$ accepts when reading a string that can be extended by 2 or more characters to reach an accepting state of $M$.

The states and transitions of $M'$ remain the same as $M$. Only the accepting states change.
"""


def should_use_dfa(M: DFA) -> bool:
    """
    This function is used to reject DFAs which aren't "interesting".

    For this problem, we consider a DFA to be interesting if there exists
    at least one state that is exactly 2 steps from an accepting state.
    """
    # Build reverse transitions
    reverse_transitions = {q: {} for q in M.states}
    for state in M.states:
        for sym in M.input_symbols:
            end_loc = M.transitions[state][sym]
            if sym not in reverse_transitions[end_loc]:
                reverse_transitions[end_loc][sym] = {state}
            else:
                reverse_transitions[end_loc][sym].add(state)

    # Check if there's any state at distance 2 from an accepting state
    states_at_distance_2 = set()
    for final in M.final_states:
        # States at distance 1 from final
        states_at_1 = set()
        for sym in M.input_symbols:
            if sym in reverse_transitions[final]:
                states_at_1.update(reverse_transitions[final][sym])

        # States at distance 2 from final
        for state_at_1 in states_at_1:
            for sym in M.input_symbols:
                if sym in reverse_transitions[state_at_1]:
                    states_at_distance_2.update(reverse_transitions[state_at_1][sym])

    return len(states_at_distance_2) > 0


def construct_M_prime(M: DFA) -> DFA:
    assert M.input_symbols == {"0", "1"}

    # Build reverse transitions to find states that are 2+ steps from accepting
    reverse_transitions = {q: {} for q in M.states}
    for state in M.states:
        for sym in M.input_symbols:
            end_loc = M.transitions[state][sym]
            if sym not in reverse_transitions[end_loc]:
                reverse_transitions[end_loc][sym] = {state}
            else:
                reverse_transitions[end_loc][sym].add(state)

    def rec_traverse(
        final_states: Set[str], state: str, have_seen: Set[str], depth: int
    ) -> None:
        if state in have_seen:
            return
        if depth >= 2:
            final_states |= {state}
            have_seen.add(state)

        for sym in M.input_symbols:
            if sym in reverse_transitions[state]:
                for n in reverse_transitions[state][sym]:
                    rec_traverse(final_states, n, have_seen, depth + 1)

    fs = set()

    for start_final in M.final_states:
        rec_traverse(fs, start_final, set(), 0)

    return DFA(
        states=M.states,
        input_symbols=M.input_symbols,
        transitions=M.transitions,
        initial_state=M.initial_state,
        final_states=fs,
    )


def generate(data: Dict[str, Any]) -> None:
    M = generate_random_dfa(3, 4)
    while not should_use_dfa(M):
        M = generate_random_dfa(3, 4)

    M_prime = construct_M_prime(M)

    # For this transformation, we ask about which states are accepting in M'
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
        M_prime,
        transitions_to_ask,
    )


def grade(data: pl.QuestionData) -> None:
    server_base.grade(data)
