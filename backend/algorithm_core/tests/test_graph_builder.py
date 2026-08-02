from algorithm_core.generator import generate_incompatible_pairs
from algorithm_core.graph_builder import build_compatibility_graph, graph_summary


def test_graph_has_a_node_per_pair():
    pairs = generate_incompatible_pairs(count=15, seed=5)
    graph = build_compatibility_graph(pairs, seed=5)
    assert graph.number_of_nodes() == 15


def test_no_self_loops():
    pairs = generate_incompatible_pairs(count=15, seed=5)
    graph = build_compatibility_graph(pairs, seed=5)
    for node in graph.nodes:
        assert node not in graph.successors(node)


def test_graph_summary_shape():
    pairs = generate_incompatible_pairs(count=10, seed=2)
    graph = build_compatibility_graph(pairs, seed=2)
    summary = graph_summary(graph)
    assert summary["total_pairs"] == 10
    assert "total_possible_swaps" in summary
    assert "average_connections_per_pair" in summary


def test_node_carries_pair_data():
    pairs = generate_incompatible_pairs(count=5, seed=9)
    graph = build_compatibility_graph(pairs, seed=9)
    first_pair = pairs[0]
    node_data = graph.nodes[first_pair.pair_id]
    assert node_data["pair"].pair_id == first_pair.pair_id
