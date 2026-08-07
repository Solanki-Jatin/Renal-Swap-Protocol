import time

from fastapi import APIRouter

from algorithm_core.greedy_matcher import solve_greedy_matching

from ..pipeline import build_pipeline, pairs_to_nodes, graph_to_edges
from ..schemas.dataset import GenerateDatasetRequest
from ..schemas.graph import GraphNode
from ..schemas.match import ImpactSummary, MatchResponse

router = APIRouter(prefix="/match", tags=["match"])


def _impact_summary(total_pairs: int, matched_pairs: int) -> ImpactSummary:
    return ImpactSummary(
        total_pairs=total_pairs,
        matched_pairs=matched_pairs,
        unmatched_pairs=total_pairs - matched_pairs,
    )


@router.post("/optimal", response_model=MatchResponse)
def match_optimal(request: GenerateDatasetRequest) -> MatchResponse:
    """
    Runs the full pipeline and solves for the mathematically optimal
    set of non overlapping exchange cycles, using the ILP solver.
    This is the endpoint that proves the project's core claim, that
    solving this properly beats a greedy shortcut.
    """
    # Imported inside the function, not at module load time, so the
    # API can still start up and serve every other route even in an
    # environment where OR-Tools isn't installed yet.
    from algorithm_core.optimal_matcher import solve_optimal_matching

    pairs, graph, cycles = build_pipeline(request.count, request.hospital_ids, request.seed)

    start = time.perf_counter()
    result = solve_optimal_matching(cycles)
    runtime_ms = (time.perf_counter() - start) * 1000

    return MatchResponse(
        nodes=[GraphNode(**node) for node in pairs_to_nodes(pairs)],
        edges=graph_to_edges(graph),
        matched_cycles=[list(cycle) for cycle in result.selected_cycles],
        impact_summary=_impact_summary(len(pairs), result.matched_pairs),
        matcher="optimal",
        solver_status=result.status,
        runtime_ms=round(runtime_ms, 2),
    )


@router.post("/greedy", response_model=MatchResponse)
def match_greedy(request: GenerateDatasetRequest) -> MatchResponse:
    """
    Runs the full pipeline and solves with the fast greedy baseline,
    for direct comparison against the optimal endpoint above. Returns
    the same response shape so the frontend can reuse one component
    for both.
    """
    pairs, graph, cycles = build_pipeline(request.count, request.hospital_ids, request.seed)

    start = time.perf_counter()
    result = solve_greedy_matching(cycles)
    runtime_ms = (time.perf_counter() - start) * 1000

    return MatchResponse(
        nodes=[GraphNode(**node) for node in pairs_to_nodes(pairs)],
        edges=graph_to_edges(graph),
        matched_cycles=[list(cycle) for cycle in result.selected_cycles],
        impact_summary=_impact_summary(len(pairs), result.matched_pairs),
        matcher="greedy",
        solver_status=None,
        runtime_ms=round(runtime_ms, 2),
    )
