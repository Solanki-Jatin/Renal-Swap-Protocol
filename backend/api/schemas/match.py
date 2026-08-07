from typing import Dict, List, Optional

from pydantic import BaseModel

from .graph import GraphNode


class ImpactSummary(BaseModel):
    """
    The numbers behind the frontend's impact dashboard: how many
    patients were in the pool, and how many actually got matched.
    """
    total_pairs: int
    matched_pairs: int
    unmatched_pairs: int


class MatchResponse(BaseModel):
    """
    Shared response shape for both /match/optimal and /match/greedy,
    so the frontend can render either one with the same component,
    just by checking the "matcher" field.
    """
    nodes: List[GraphNode]
    edges: List[Dict[str, str]]
    matched_cycles: List[List[str]]
    impact_summary: ImpactSummary
    matcher: str
    solver_status: Optional[str] = None
    runtime_ms: float
