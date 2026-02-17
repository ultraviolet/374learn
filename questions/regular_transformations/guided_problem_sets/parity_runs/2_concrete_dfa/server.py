import random
from itertools import product
from typing import Any, Dict

import prairielearn as pl
import theorielearn.regular_transformation_concrete_example.server_base as server_base
from theorielearn.automata_utils.fa_utils import generate_random_dfa
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA, NFATransitionsT


TRANSFORMATION_NAME = "PARITY_RUNS"

TRANSFORMATION_DEFINITION = r"""
Given a language $L \subseteq \{0,1\}^*$, we define
$$L' = \{w \in \Sigma^* \mid \mathit{parity\_runs}(w) \in L\}$$

where $\mathit{parity\_runs}(w)$ returns the string formed by replacing each maximal substring of identical bits in $w$ with $1$ if the length of the substring is odd, and with $0$ if the length is even.

For example, $\mathit{parity\_runs}(11000010) = 0011$.
"""

DESCRIPTION_OF_STATES = r"""
Intuitively, as $M'$ reads the input string, it needs to track runs of identical bits and determine their parity before feeding the result to the simulation of $M$. The NFA needs to:
1. Track the current bit value being read in a run
2. Count the parity (odd/even) of the current run length
3. When the run ends (either by reading a different bit or reaching end of string), emit the appropriate bit (1 for odd length, 0 for even length) to the simulation of $M$

For each state $q$ in the DFA $M$, we will have multiple states in $M'$ to track:
- Which bit value (0 or 1) we're currently reading in a run
- Whether the current run length is odd or even
- The current state in the simulation of $M$

Specifically, every state $q$ in the DFA $M$ will correspond to five states in $M'$:

- The state $(q, \text{start})$ means we're at the beginning (haven't read any bits yet) and the simulation of $M$ is in state $q$.
- The state $(q, \text{read0\_odd})$ means we just read an odd number of $0$s in the current run, and the simulation is in state $q$.
- The state $(q, \text{read0\_even})$ means we just read an even number of $0$s in the current run, and the simulation is in state $q$.
- The state $(q, \text{read1\_odd})$ means we just read an odd number of $1$s in the current run, and the simulation is in state $q$.
- The state $(q, \text{read1\_even})$ means we just read an even number of $1$s in the current run, and the simulation is in state $q$.
"""

START = "start"
READ0_ODD = "read0_odd"
READ0_EVEN = "read0_even"
READ1_ODD = "read1_odd"
READ1_EVEN = "read1_even"
STATE_LABELS = [START, READ0_ODD, READ0_EVEN, READ1_ODD, READ1_EVEN]


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

    transitions: NFATransitionsT = {q_prime: dict() for q_prime in states}
    for q in M.states:
        # From start state:
        # - On 0: start reading 0s (go to read0_odd with count 1)
        transitions[(q, START)]["0"] = {(q, READ0_ODD)}
        # - On 1: start reading 1s (go to read1_odd with count 1)
        transitions[(q, START)]["1"] = {(q, READ1_ODD)}

        # From read0_odd state (just read odd number of 0s):
        # - On 0: continue run, now even (go to read0_even)
        transitions[(q, READ0_ODD)]["0"] = {(q, READ0_EVEN)}
        # - On 1: run ends, emit 1 (odd length) to M, start new run of 1s
        #         emit 1 means: take transition δ(q, 1) in M, then go to read1_odd
        transitions[(q, READ0_ODD)]["1"] = {(M.transitions[q]["1"], READ1_ODD)}

        # From read0_even state (just read even number of 0s):
        # - On 0: continue run, now odd (go to read0_odd)
        transitions[(q, READ0_EVEN)]["0"] = {(q, READ0_ODD)}
        # - On 1: run ends, emit 0 (even length) to M, start new run of 1s
        #         emit 0 means: take transition δ(q, 0) in M, then go to read1_odd
        transitions[(q, READ0_EVEN)]["1"] = {(M.transitions[q]["0"], READ1_ODD)}

        # From read1_odd state (just read odd number of 1s):
        # - On 1: continue run, now even (go to read1_even)
        transitions[(q, READ1_ODD)]["1"] = {(q, READ1_EVEN)}
        # - On 0: run ends, emit 1 (odd length) to M, start new run of 0s
        #         emit 1 means: take transition δ(q, 1) in M, then go to read0_odd
        transitions[(q, READ1_ODD)]["0"] = {(M.transitions[q]["1"], READ0_ODD)}

        # From read1_even state (just read even number of 1s):
        # - On 1: continue run, now odd (go to read1_odd)
        transitions[(q, READ1_EVEN)]["1"] = {(q, READ1_ODD)}
        # - On 0: run ends, emit 0 (even length) to M, start new run of 0s
        #         emit 0 means: take transition δ(q, 0) in M, then go to read0_odd
        transitions[(q, READ1_EVEN)]["0"] = {(M.transitions[q]["0"], READ0_ODD)}

    initial_state = (M.initial_state, START)

    # Accept if: we're in an accepting state of M and either
    # - we're at start (empty string case), or
    # - we just finished a run with odd length (read0_odd or read1_odd), or
    # - we just finished a run with even length (read0_even or read1_even)
    # All of these correspond to completing the parity_runs transformation
    final_states = set()
    for q in M.final_states:
        final_states.add((q, READ0_ODD))
        final_states.add((q, READ0_EVEN))
        final_states.add((q, READ1_ODD))
        final_states.add((q, READ1_EVEN))
    # Special case: if initial state is accepting in M, then empty string should be accepted
    if M.initial_state in M.final_states:
        final_states.add((M.initial_state, START))

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
