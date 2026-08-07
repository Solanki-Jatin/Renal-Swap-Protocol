from fastapi import APIRouter

from algorithm_core.graph_builder import graph_summary as compute_graph_summary

from ..pipeline import build_pipeline, pairs_to_nodes, graph_to_edges
from ..schemas.dataset import GenerateDatasetRequest
from ..schemas.graph import GraphBuildResponse, GraphNode, GraphSummary

router = APIRouter(prefix="/graph", tags=["graph"])


@router.post("/build", response_model=GraphBuildResponse)
def build_graph(request: GenerateDatasetRequest) -> GraphBuildResponse:
    """
    Generates a pool and builds the compatibility graph from it,
    returning nodes and edges in the exact shape the frontend's graph
    view was built against.
    """
    pairs, graph, _cycles = build_pipeline(request.count, request.hospital_ids, request.seed)

    nodes = [GraphNode(**node) for node in pairs_to_nodes(pairs)]
    edges = graph_to_edges(graph)
    summary = GraphSummary(**compute_graph_summary(graph))

    return GraphBuildResponse(nodes=nodes, edges=edges, summary=summary)
