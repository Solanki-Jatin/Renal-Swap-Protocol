"""
Finds every valid exchange cycle in the compatibility graph, bounded to
length 2 and 3, which is the length real kidney exchange programs use
in practice. Every transplant in a cycle has to happen on the same
day, in every hospital involved, since no donor can be asked to wait
and risk the other side of the swap falling through. That constraint
is why cycles longer than 3 are excluded here.

A cycle is a closed loop of pairs where each pair's donor can give to
the next pair's patient, and the last pair's donor can give back to
the first pair's patient. A 2 cycle is a direct two-way swap, a 3
cycle is a three-way swap.

The search itself uses NetworkX's implementation of Johnson's
algorithm for finding simple cycles. What this module adds on top is
the domain specific framing: bounding to a realistic length, and
scoring each candidate cycle so the next phase (the optimal and greedy
matchers) has something to decide between.
"""

from typing import List, Tuple

import networkx as nx

MIN_CYCLE_LENGTH = 2
MAX_CYCLE_LENGTH = 3


def find_candidate_cycles(
    graph: nx.DiGraph,
    max_length: int = MAX_CYCLE_LENGTH,
) -> List[Tuple[str, ...]]:
    """
    Returns every simple directed cycle in the graph with length
    between 2 and max_length inclusive. Each cycle is a tuple of pair
    ids, in the order the swap would happen.

    max_length defaults to 3, matching the real world constraint that
    every transplant in a cycle must happen simultaneously.
    """
    if max_length < MIN_CYCLE_LENGTH:
        raise ValueError(f"max_length must be at least {MIN_CYCLE_LENGTH}")

    cycles = []
    for cycle in nx.simple_cycles(graph, length_bound=max_length):
        if len(cycle) >= MIN_CYCLE_LENGTH:
            cycles.append(tuple(cycle))
    return cycles


def cycle_value(cycle: Tuple[str, ...]) -> int:
    """
    A simple value score for a cycle, right now just the number of
    patients it matches, which equals its length. This is the hook
    the next phase will extend into a weighted score, for example
    giving extra priority to rare blood types or highly sensitized
    patients who are otherwise hard to match.
    """
    return len(cycle)


def cycles_summary(cycles: List[Tuple[str, ...]]) -> dict:
    """A quick, readable breakdown of how many 2-way versus 3-way cycles were found."""
    two_way = sum(1 for cycle in cycles if len(cycle) == 2)
    three_way = sum(1 for cycle in cycles if len(cycle) == 3)
    return {
        "total_candidate_cycles": len(cycles),
        "two_way_swaps": two_way,
        "three_way_swaps": three_way,
    }
