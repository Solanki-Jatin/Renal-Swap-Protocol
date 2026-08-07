from typing import List, Optional

from fastapi import APIRouter, Query

from ..schemas.benchmark import BenchmarkResponse, BenchmarkRow

router = APIRouter(tags=["benchmark"])


@router.get("/benchmark", response_model=BenchmarkResponse)
def get_benchmark(
    pool_sizes: Optional[str] = Query(
        default=None,
        description="Comma separated pool sizes to benchmark, for example 50,200,1000. Defaults to the project's standard set.",
    )
) -> BenchmarkResponse:
    """
    Runs the optimal vs greedy benchmark across a range of pool sizes
    and returns match rate and runtime for both. Defaults to the same
    pool sizes used in the README's Benchmarks table.
    """
    # Imported here rather than at module load time, since running
    # the benchmark requires OR-Tools for its optimal matcher half.
    from benchmarks.run_benchmarks import run_all_benchmarks

    sizes: Optional[List[int]] = None
    if pool_sizes:
        sizes = [int(size.strip()) for size in pool_sizes.split(",") if size.strip()]

    results = run_all_benchmarks(sizes)
    rows = [BenchmarkRow(**row) for row in results]
    return BenchmarkResponse(results=rows)
