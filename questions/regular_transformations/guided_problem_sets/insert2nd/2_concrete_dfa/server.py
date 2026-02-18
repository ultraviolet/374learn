import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA, DFATransitionsT


TRANSFORMATION_NAME = "INSERT2ND"

TRANSFORMATION_DEFINITION = r"""
For any non-empty string $w$ with $|w| \geq 2$, let $\mathsf{Delete2nd}(w)$ denote the string
obtained by deleting the second symbol in $w$.

Given a language $L \subseteq \{0,1\}^*$, we define
$$\mathsf{INSERT2ND}(L) = \{ w \in \Sigma^* \mid |w| \geq 2 \text{ and } \mathsf{Delete2nd}(w) \in L \}$$

In other words, $\mathsf{INSERT2ND}(L)$ contains all strings of length $\geq 2$ whose second character
can be deleted to produce a string in $L$.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, $M'$ reads the input string and simulates $M$, but skips the second input symbol.
We track how many symbols $M'$ has read so far:

Every state $q$ in the DFA $M$ will correspond to three states in $M'$, as described below:

- The state $(q, 0)$ means that $M$ is in state $q$ and $M'$ has read **0** symbols so far.
- The state $(q, 1)$ means that $M$ is in state $q$ and $M'$ has read exactly **1** symbol (and has fed it to $M$).
- The state $(q, \text{many})$ means that $M$ is in state $q$ and $M'$ has read **more than 1** symbol (the second symbol was discarded, all others fed to $M$).

$M'$ accepts when $M$ is in an accepting state and $M'$ has read at least 2 symbols (counter = many).
"""

ZERO = "0"
ONE = "1"
MANY = "many"
STATE_LABELS = [ZERO, ONE, MANY]


def should_use_dfa(M: DFA) -> bool:
    """Reject DFAs which aren't 'interesting': require that transitions are non-trivial."""
    return all(
        M.transitions[q]["0"] != q or M.transitions[q]["1"] != q
        for q in M.states
    )


def construct_M_prime(M: DFA) -> DFA:
    assert M.input_symbols == {"0", "1"}

    states = set(product(M.states, STATE_LABELS))
    transitions: DFATransitionsT = {}

    for q in M.states:
        # From state (q, 0): read 0 symbols so far
        # On any symbol a: pass to M (go to δ(q,a)), advance counter to 1
        transitions[(q, ZERO)] = {
            "0": (M.transitions[q]["0"], ONE),
            "1": (M.transitions[q]["1"], ONE),
        }

        # From state (q, 1): read exactly 1 symbol so far
        # On any symbol a: DISCARD it (second symbol), advance counter to many
        transitions[(q, ONE)] = {
            "0": (q, MANY),
            "1": (q, MANY),
        }

        # From state (q, many): read > 1 symbol so far
        # On any symbol a: pass to M normally
        transitions[(q, MANY)] = {
            "0": (M.transitions[q]["0"], MANY),
            "1": (M.transitions[q]["1"], MANY),
        }

    initial_state = (M.initial_state, ZERO)
    final_states = set(product(M.final_states, {MANY}))

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

    q = random.choice(list(M.states))
    transitions_to_ask = [
        ((q, ZERO), "0"),
        ((q, ZERO), "1"),
        ((q, ONE), "0"),
        ((q, ONE), "1"),
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
