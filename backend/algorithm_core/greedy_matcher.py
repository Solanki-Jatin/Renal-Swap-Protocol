"""
Greedy baseline matcher, kept purely as a comparison point against the
optimal ILP matcher.

The strategy is simple: sort every candidate cycle by how many patients
it matches, then walk down that list picking each cycle as long as none
of its pairs have already been used by a cycle picked earlier. This is
fast, roughly O(n log n) for the sort plus a linear pass, compared to
the ILP solver which can take meaningfully longer on large pools.

The reason to keep this alongside the optimal matcher is not that
greedy is bad, it is fast and often reasonably close to optimal, but it
can be proven wrong: a single large cycle picked early can block
several smaller cycles that, added together, would have matched more
patients than the one large cycle did. The benchmark suite quantifies
exactly how often, and by how much, this happens, which is the whole
point of keeping both matchers in the project.
"""

from typing import List, Set, Tuple

from .cycle_finder import cycle_value


class GreedyMatchResult:
    """Holds the outcome of a single greedy matching run."""

    def __init__(self, selected_cycles: List[Tuple[str, ...]], matched_pairs: int):
        self.selected_cycles = selected_cycles
        self.matched_pairs = matched_pairs

    def to_dict(self) -> dict:
        return {
            "selected_cycles": [list(cycle) for cycle in self.selected_cycles],
            "matched_pairs": self.matched_pairs,
            "cycles_used": len(self.selected_cycles),
        }


def solve_greedy_matching(candidate_cycles: List[Tuple[str, ...]]) -> GreedyMatchResult:
    """
    Selects cycles greedily, highest value first, skipping any cycle
    that shares a pair with one already selected.

    Ties in value are broken by the order the cycles were given in,
    which in practice means the order cycle_finder discovered them.
    """
    ordered_cycles = sorted(candidate_cycles, key=cycle_value, reverse=True)

    used_pairs: Set[str] = set()
    selected_cycles: List[Tuple[str, ...]] = []

    for cycle in ordered_cycles:
        if any(pair_id in used_pairs for pair_id in cycle):
            continue
        selected_cycles.append(cycle)
        used_pairs.update(cycle)

    matched_pairs = sum(cycle_value(cycle) for cycle in selected_cycles)
    return GreedyMatchResult(selected_cycles=selected_cycles, matched_pairs=matched_pairs)
