"""
Builds the directed compatibility graph used by the matching algorithms.

Each incompatible pair becomes a node. A directed edge is added from
pair A to pair B whenever pair A's donor could give a kidney to pair
B's patient. This graph is the single shared structure that both the
cycle enumerator and the optimal and greedy matchers will operate on
in the next phases.
"""

import random
from typing import List, Optional

import networkx as nx

from .models import IncompatiblePair
from .compatibility import is_compatible


def build_compatibility_graph(
    pairs: List[IncompatiblePair],
    seed: Optional[int] = None,
) -> nx.DiGraph:
    """
    Returns a directed graph where nodes are pair ids and an edge
    A -> B means pair A's donor is compatible with pair B's patient.

    Each node carries the full IncompatiblePair object as node data
    under the "pair" attribute, so downstream code can read blood
    types, hospital ids, and sensitization status without a separate
    lookup table.
    """
    rng = random.Random(seed)
    graph = nx.DiGraph()

    for pair in pairs:
        graph.add_node(pair.pair_id, pair=pair)

    for pair_a in pairs:
        for pair_b in pairs:
            if pair_a.pair_id == pair_b.pair_id:
                continue
            if is_compatible(
                pair_a.donor.blood_type,
                pair_b.patient.blood_type,
                pair_b.patient.sensitized,
                rng,
            ):
                graph.add_edge(pair_a.pair_id, pair_b.pair_id)

    return graph


def graph_summary(graph: nx.DiGraph) -> dict:
    """
    A small, human readable summary of the graph. Useful for printing
    to the terminal during development, and later for returning from
    an API endpoint as a quick sanity check on how connected the
    current pool is.
    """
    node_count = graph.number_of_nodes()
    edge_count = graph.number_of_edges()
    return {
        "total_pairs": node_count,
        "total_possible_swaps": edge_count,
        "average_connections_per_pair": (
            round(edge_count / node_count, 2) if node_count > 0 else 0
        ),
    }
