from algorithm_core.optimal_matcher import solve_optimal_matching


def test_no_candidates_returns_empty_result():
    result = solve_optimal_matching([])
    assert result.matched_pairs == 0
    assert result.selected_cycles == []
    assert result.status == "NO_CANDIDATES"


def test_non_overlapping_cycles_are_both_selected():
    cycles = [("a", "b"), ("c", "d")]
    result = solve_optimal_matching(cycles)
    assert result.matched_pairs == 4
    assert len(result.selected_cycles) == 2


def test_overlapping_cycles_pick_the_higher_value_one():
    # "a" appears in both cycles, so they cannot both be selected.
    # The 3-way cycle matches more patients than the 2-way cycle,
    # so the optimal solver should prefer it over the smaller one.
    cycles = [("a", "b"), ("a", "c", "d")]
    result = solve_optimal_matching(cycles)
    assert result.matched_pairs == 3
    assert result.selected_cycles == [("a", "c", "d")]


def test_no_pair_appears_in_more_than_one_selected_cycle():
    cycles = [("a", "b"), ("b", "c"), ("c", "d")]
    result = solve_optimal_matching(cycles)
    used_pairs = [pair_id for cycle in result.selected_cycles for pair_id in cycle]
    assert len(used_pairs) == len(set(used_pairs))


def test_to_dict_shape():
    cycles = [("a", "b")]
    result = solve_optimal_matching(cycles)
    data = result.to_dict()
    assert data["matched_pairs"] == 2
    assert data["cycles_used"] == 1
    assert "status" in data
    assert "selected_cycles" in data
