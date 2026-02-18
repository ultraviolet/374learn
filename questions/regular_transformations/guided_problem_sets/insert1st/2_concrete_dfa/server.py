import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA, DFATransitionsT


TRANSFORMATION_NAME = "INSERT1ST"

TRANSFORMATION_DEFINITION = r"""
For any non-empty string $w$, let $\mathsf{Delete1st}(w)$ denote the string obtained by
deleting the **entire first maximal run** of identical symbols from $w$.

Given a language $L \subseteq \{0,1\}^*$, we define
$$\mathsf{INSERT1ST}(L) = \{ w \in \{0,1\}^* \mid w \neq \varepsilon \text{ and } \mathsf{Delete1st}(w) \in L \}$$

In other words, $\mathsf{INSERT1ST}(L)$ contains all non-empty strings $w$ such that
deleting the first maximal run of identical symbols from $w$ yields a string in $L$.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, $M'$ reads the input string and simulates $M$ on the string after the first run
is removed. We track the current phase of reading using four labels:

Every state $q$ in the DFA $M$ will correspond to four states in $M'$, as described below:

- The state $(q, \text{start})$ means that $M$ is in state $q$ and $M'$ has read **no symbols** yet.
- The state $(q, \text{first0})$ means that $M$ is in state $q$, and $M'$ is currently reading
  the first maximal run of **0**s (these 0s have not been fed to $M$ yet).
- The state $(q, \text{first1})$ means that $M$ is in state $q$, and $M'$ is currently reading
  the first maximal run of **1**s (these 1s have not been fed to $M$ yet).
- The state $(q, \text{after})$ means that $M$ is in state $q$, and $M'$ has **finished**
  reading the first run and is now simulating $M$ normally on the remaining input.

$M'$ accepts when $M$ is in an accepting state and $M'$ has finished reading the first run
(or has read all of a single-run string, which has $\mathsf{Delete1st}$ equal to $\varepsilon$).
"""

START = "start"
FIRST0 = "first0"
FIRST1 = "first1"
AFTER = "after"
STATE_LABELS = [START, FIRST0, FIRST1, AFTER]


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
        # (q, start): read 0 symbols so far
        # On 0: start first run of 0s (don't feed to M yet)
        # On 1: start first run of 1s (don't feed to M yet)
        transitions[(q, START)] = {
            "0": (q, FIRST0),
            "1": (q, FIRST1),
        }

        # (q, first0): inside the first run of 0s, M hasn't advanced
        # On 0: stay in first run of 0s
        # On 1: first run ended; feed this 1 to M, go to after
        transitions[(q, FIRST0)] = {
            "0": (q, FIRST0),
            "1": (M.transitions[q]["1"], AFTER),
        }

        # (q, first1): inside the first run of 1s, M hasn't advanced
        # On 1: stay in first run of 1s
        # On 0: first run ended; feed this 0 to M, go to after
        transitions[(q, FIRST1)] = {
            "1": (q, FIRST1),
            "0": (M.transitions[q]["0"], AFTER),
        }

        # (q, after): first run finished, simulate M normally
        transitions[(q, AFTER)] = {
            "0": (M.transitions[q]["0"], AFTER),
            "1": (M.transitions[q]["1"], AFTER),
        }

    initial_state = (M.initial_state, START)
    # Accept if M is in accepting state and we've finished the first run
    # (either in "after" mode, or the whole string was a single run => first0/first1)
    final_states = set(product(M.final_states, {AFTER, FIRST0, FIRST1}))

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
        ((q, START), "0"),
        ((q, START), "1"),
        ((q, FIRST0), "0"),
        ((q, FIRST0), "1"),
        ((q, FIRST1), "0"),
        ((q, FIRST1), "1"),
        ((q, AFTER), "0"),
        ((q, AFTER), "1"),
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
