import networkx as nx

from algorithm_core.cycle_finder import find_candidate_cycles, cycle_value, cycles_summary
from algorithm_core.generator import generate_incompatible_pairs
from algorithm_core.graph_builder import build_compatibility_graph


def test_finds_a_two_way_cycle():
    graph = nx.DiGraph()
    graph.add_edge("a", "b")
    graph.add_edge("b", "a")

    cycles = find_candidate_cycles(graph)
    assert len(cycles) == 1
    assert set(cycles[0]) == {"a", "b"}


def test_finds_a_three_way_cycle():
    graph = nx.DiGraph()
    graph.add_edge("a", "b")
    graph.add_edge("b", "c")
    graph.add_edge("c", "a")

    cycles = find_candidate_cycles(graph)
    assert len(cycles) == 1
    assert len(cycles[0]) == 3


def test_ignores_cycles_longer_than_max_length():
    graph = nx.DiGraph()
    graph.add_edge("a", "b")
    graph.add_edge("b", "c")
    graph.add_edge("c", "d")
    graph.add_edge("d", "a")

    cycles = find_candidate_cycles(graph, max_length=3)
    assert cycles == []


def test_no_cycles_in_an_acyclic_graph():
    graph = nx.DiGraph()
    graph.add_edge("a", "b")
    graph.add_edge("b", "c")

    assert find_candidate_cycles(graph) == []


def test_cycle_value_equals_length():
    assert cycle_value(("a", "b")) == 2
    assert cycle_value(("a", "b", "c")) == 3


def test_cycles_summary_counts_correctly():
    cycles = [("a", "b"), ("c", "d"), ("e", "f", "g")]
    summary = cycles_summary(cycles)
    assert summary["total_candidate_cycles"] == 3
    assert summary["two_way_swaps"] == 2
    assert summary["three_way_swaps"] == 1


def test_cycles_found_on_a_realistic_generated_pool():
    pairs = generate_incompatible_pairs(count=40, seed=42)
    graph = build_compatibility_graph(pairs, seed=42)
    cycles = find_candidate_cycles(graph)

    assert isinstance(cycles, list)
    for cycle in cycles:
        assert len(cycle) in (2, 3)
