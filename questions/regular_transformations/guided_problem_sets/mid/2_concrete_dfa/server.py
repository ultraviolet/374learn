import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "MID"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{w \mid xwy \in L ~\text{for some}~ x,y \in \Sigma^*\}$$

In other words, $w \in L'$ if and only if $w$ appears as a substring of some string in $L$.

For example, if $L$ contains $0110$, then $L'$ contains $\varepsilon$, $0$, $1$, $01$, $11$, $10$, $011$, $110$, and $0110$.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, the NFA $M'$ needs to non-deterministically guess where the substring $w$ starts and ends within a string from $L$. The construction uses three phases:

- **Simulating $x$**: $M'$ starts by non-deterministically simulating $M$ to account for the prefix $x$. At any point, it can guess that $w$ is about to begin.
- **Reading $w$**: Once $M'$ guesses that $w$ has started, it stops simulating and just reads the input $w$ directly, keeping track of where in $M$ the simulation is.
- **Simulating $y$**: After reading all of $w$, $M'$ non-deterministically continues simulating $M$ to account for the suffix $y$, and accepts if this simulation can reach an accepting state.

We use three labels for states:
- $(q, \text{simulatingX})$: currently simulating the prefix $x$ in state $q$ of $M$
- $(q, \text{readingW})$: currently reading the input $w$, having reached state $q$ after processing $x$
- $(q, \text{simulatingY})$: currently simulating the suffix $y$ in state $q$ of $M$

The key transitions are:
- From $(q, \text{simulatingX})$: On any symbol, can continue simulating (epsilon transition then symbol), or can guess $w$ starts now (epsilon transition to readingW)
- From $(q, \text{readingW})$: On any symbol, read it directly and move to the next state in readingW mode, or guess $w$ ends now (epsilon transition to simulatingY)
- From $(q, \text{simulatingY})$: On epsilon, can continue simulating $M$ until reaching an accepting state
"""

SIMULATING_X = "simulatingX"
READING_W = "readingW"
SIMULATING_Y = "simulatingY"
STATE_LABELS = [SIMULATING_X, READING_W, SIMULATING_Y]


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

    states = set(product(M.states, STATE_LABELS))

    transitions: NFATransitionsT = {q_prime: {"0": set(), "1": set(), "": set()} for q_prime in states}

    for q in M.states:
        # From simulatingX state:
        # Epsilon transition to readingW (guess w starts now)
        transitions[(q, SIMULATING_X)][""].add((q, READING_W))

        # Epsilon transition to self, then on symbol a, go to (δ(q,a), simulatingX)
        for symbol in M.input_symbols:
            transitions[(q, SIMULATING_X)][symbol].add((M.transitions[q][symbol], SIMULATING_X))

        # From readingW state:
        # On symbol a, go to (δ(q,a), readingW) - reading w directly
        for symbol in M.input_symbols:
            transitions[(q, READING_W)][symbol].add((M.transitions[q][symbol], READING_W))

        # Epsilon transition to simulatingY (guess w ends now)
        transitions[(q, READING_W)][""].add((q, SIMULATING_Y))

        # From simulatingY state:
        # Continue simulating on epsilon
        for symbol in M.input_symbols:
            transitions[(q, SIMULATING_Y)][""].add((M.transitions[q][symbol], SIMULATING_Y))

    initial_state = (M.initial_state, SIMULATING_X)

    # Accept if we're in simulatingY and the corresponding M state is accepting
    final_states = {(q, SIMULATING_Y) for q in M.final_states}

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
        ((random.choice(list(M.states)), label), a)
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
