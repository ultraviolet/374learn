import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "DELETE2ND"

TRANSFORMATION_DEFINITION = r"""
For any non-empty string $w$ with $|w| \geq 2$, let $\mathsf{Delete2nd}(w)$ denote the string
obtained by deleting the second symbol in $w$.

Given a language $L \subseteq \{0,1\}^*$, we define
$$\mathsf{DELETE2ND}(L) = \{ \mathsf{Delete2nd}(w) \mid |w| \geq 2 \text{ and } w \in L \}$$

In other words, $\mathsf{DELETE2ND}(L)$ consists of all strings obtainable from strings in $L$
(of length $\geq 2$) by deleting the second character.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, $M'$ reads the output string (after deletion) and simulates $M$ on the
original string (before deletion). $M'$ guesses non-deterministically what the deleted
second character was.

Every state $q$ in the DFA $M$ will correspond to three states in $M'$, as described below:

- The state $(q, 0)$ means that $M$ is in state $q$ and $M'$ has processed **0** output symbols
  (equivalently, $M$ has consumed 0 input symbols from the original string).
- The state $(q, 1)$ means that $M$ is in state $q$, $M'$ has processed **1** output symbol
  (so $M$ has consumed 1 input symbol), and $M'$ is about to guess the deleted second symbol.
- The state $(q, \text{many})$ means that $M$ is in state $q$ and $M'$ has processed
  **more than 1** output symbol (the second symbol has already been guessed and fed to $M$).

An $\varepsilon$-transition from state $(q, 1)$ non-deterministically guesses the deleted character.
"""

ZERO = "0"
ONE = "1"
MANY = "many"
STATE_LABELS = [ZERO, ONE, MANY]


def should_use_dfa(M: DFA) -> bool:
    """Reject DFAs that aren't 'interesting'."""
    return all(
        M.transitions[q]["0"] != q or M.transitions[q]["1"] != q
        for q in M.states
    )


def construct_M_prime(M: DFA) -> NFA:
    assert M.input_symbols == {"0", "1"}

    states = set(product(M.states, STATE_LABELS))
    transitions: NFATransitionsT = {q_prime: dict() for q_prime in states}

    for q in M.states:
        # From state (q, 0): feed first input character to M, advance to state 1
        transitions[(q, ZERO)]["0"] = {(M.transitions[q]["0"], ONE)}
        transitions[(q, ZERO)]["1"] = {(M.transitions[q]["1"], ONE)}
        transitions[(q, ZERO)][""] = set()

        # From state (q, 1): use epsilon to guess the deleted second character
        # Non-deterministically pick 0 or 1 as the deleted character, feed to M
        transitions[(q, ONE)]["0"] = set()  # No direct transitions on input symbols
        transitions[(q, ONE)]["1"] = set()
        transitions[(q, ONE)][""] = {
            (M.transitions[q]["0"], MANY),  # Guess deleted char was 0
            (M.transitions[q]["1"], MANY),  # Guess deleted char was 1
        }

        # From state (q, many): feed remaining characters to M normally
        transitions[(q, MANY)]["0"] = {(M.transitions[q]["0"], MANY)}
        transitions[(q, MANY)]["1"] = {(M.transitions[q]["1"], MANY)}
        transitions[(q, MANY)][""] = set()

    initial_state = (M.initial_state, ZERO)
    final_states = set(product(M.final_states, {MANY}))

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

    q = random.choice(list(M.states))
    transitions_to_ask = [
        ((q, ZERO), "0"),
        ((q, ZERO), "1"),
        ((q, ONE), ""),   # epsilon transition - the interesting one
        ((q, MANY), "0"),
        ((q, MANY), "1"),
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
