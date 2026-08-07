from typing import Dict, List

from pydantic import BaseModel


class GraphNode(BaseModel):
    """One pair, represented as a graph node for the frontend's graph view."""
    id: str
    patient_blood_type: str
    donor_blood_type: str


class GraphSummary(BaseModel):
    total_pairs: int
    total_possible_swaps: int
    average_connections_per_pair: float


class GraphBuildResponse(BaseModel):
    nodes: List[GraphNode]
    # Each edge is a plain dict with "from" and "to" keys, matching
    # the exact shape given to the frontend in the handover guide.
    # A strict model isn't used here because "from" is a reserved
    # Python keyword and not worth the extra aliasing complexity.
    edges: List[Dict[str, str]]
    summary: GraphSummary
