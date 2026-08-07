"""
Direct comparison between the greedy baseline and the optimal ILP
matcher, on the same input. This is what actually proves the value of
building the optimal matcher at all, rather than just shipping greedy.

Needs OR-Tools installed to run, since it imports the optimal matcher.
"""

from algorithm_core.cycle_finder import find_candidate_cycles
from algorithm_core.generator import generate_incompatible_pairs
from algorithm_core.graph_builder import build_compatibility_graph
from algorithm_core.greedy_matcher import solve_greedy_matching
from algorithm_core.optimal_matcher import solve_optimal_matching


def test_optimal_never_does_worse_than_greedy_on_a_realistic_pool():
    pairs = generate_incompatible_pairs(count=40, seed=42)
    graph = build_compatibility_graph(pairs, seed=42)
    cycles = find_candidate_cycles(graph)

    greedy_result = solve_greedy_matching(cycles)
    optimal_result = solve_optimal_matching(cycles)

    # the optimal solver can never do worse than greedy, since greedy's
    # own selection is always itself a feasible, if not optimal, answer
    assert optimal_result.matched_pairs >= greedy_result.matched_pairs


def test_optimal_strictly_beats_greedy_on_its_known_blind_spot():
    cycles = [
        ("a", "b", "c"),
        ("a", "d"),
        ("b", "e"),
        ("c", "f"),
    ]
    greedy_result = solve_greedy_matching(cycles)
    optimal_result = solve_optimal_matching(cycles)

    assert greedy_result.matched_pairs == 3
    assert optimal_result.matched_pairs == 6
    assert optimal_result.matched_pairs > greedy_result.matched_pairs
