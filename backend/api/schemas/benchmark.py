from typing import List

from pydantic import BaseModel


class BenchmarkRow(BaseModel):
    pool_size: int
    candidate_cycles: int
    optimal_matched: int
    greedy_matched: int
    optimal_time_ms: float
    greedy_time_ms: float
    solver_status: str


class BenchmarkResponse(BaseModel):
    results: List[BenchmarkRow]
