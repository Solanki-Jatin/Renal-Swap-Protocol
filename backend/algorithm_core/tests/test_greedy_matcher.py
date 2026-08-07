from algorithm_core.greedy_matcher import solve_greedy_matching


def test_no_candidates_returns_empty_result():
    result = solve_greedy_matching([])
    assert result.matched_pairs == 0
    assert result.selected_cycles == []


def test_non_overlapping_cycles_are_both_selected():
    cycles = [("a", "b"), ("c", "d")]
    result = solve_greedy_matching(cycles)
    assert result.matched_pairs == 4
    assert len(result.selected_cycles) == 2


def test_prefers_higher_value_cycle_when_cycles_conflict():
    cycles = [("a", "b"), ("a", "c", "d")]
    result = solve_greedy_matching(cycles)
    assert result.selected_cycles == [("a", "c", "d")]
    assert result.matched_pairs == 3


def test_no_pair_used_twice():
    cycles = [("a", "b"), ("b", "c"), ("c", "d")]
    result = solve_greedy_matching(cycles)
    used_pairs = [pair_id for cycle in result.selected_cycles for pair_id in cycle]
    assert len(used_pairs) == len(set(used_pairs))


def test_greedy_can_be_suboptimal():
    """
    This is the whole point of keeping both matchers. A single large
    cycle can greedily block several smaller cycles that, combined,
    would have matched more patients. Here, the true optimal answer
    is 6 (three separate 2-way swaps), but greedy picks the one 3-way
    cycle first, since it has the highest individual value, and ends
    up matching only 3 patients as a result.

    The optimal solver's side of this exact scenario is verified
    against this one in test_greedy_vs_optimal.py.
    """
    cycles = [
        ("a", "b", "c"),  # value 3, picked first by greedy
        ("a", "d"),       # value 2, blocked once "a" is used
        ("b", "e"),       # value 2, blocked once "b" is used
        ("c", "f"),       # value 2, blocked once "c" is used
    ]
    result = solve_greedy_matching(cycles)
    assert result.matched_pairs == 3
    assert result.selected_cycles == [("a", "b", "c")]
