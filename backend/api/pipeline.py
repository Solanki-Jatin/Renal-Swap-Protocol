"""
Shared helper that runs the dataset, graph, and cycle detection steps
once, so every route that needs this pipeline (graph/build, both
match endpoints) doesn't repeat the same three function calls. This
file has no route decorators in it, it's pure logic, kept separate
so it can be unit tested without spinning up the API at all.
"""

from typing import List, Optional, Tuple

import networkx as nx

from algorithm_core.generator import generate_incompatible_pairs
from algorithm_core.graph_builder import build_compatibility_graph
from algorithm_core.cycle_finder import find_candidate_cycles
from algorithm_core.models import IncompatiblePair


def build_pipeline(
    count: int,
    hospital_ids: Optional[List[str]] = None,
    seed: Optional[int] = None,
) -> Tuple[List[IncompatiblePair], nx.DiGraph, list]:
    """Generates pairs, builds the graph, and finds candidate cycles, in one call."""
    pairs = generate_incompatible_pairs(count=count, hospital_ids=hospital_ids, seed=seed)
    graph = build_compatibility_graph(pairs, seed=seed)
    cycles = find_candidate_cycles(graph)
    return pairs, graph, cycles


def pairs_to_nodes(pairs: List[IncompatiblePair]) -> List[dict]:
    """Converts pairs into the plain dict shape GraphNode expects."""
    return [
        {
            "id": pair.pair_id,
            "patient_blood_type": pair.patient.blood_type.value,
            "donor_blood_type": pair.donor.blood_type.value,
        }
        for pair in pairs
    ]


def graph_to_edges(graph: nx.DiGraph) -> List[dict]:
    """Converts the NetworkX graph's edges into the frontend's expected {from, to} shape."""
    return [{"from": source, "to": target} for source, target in graph.edges()]
