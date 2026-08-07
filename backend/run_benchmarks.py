"""
Benchmark suite comparing the optimal ILP matcher against the greedy
baseline matcher, across a range of pool sizes. This is what turns
"the optimal solver is better" from a claim into an actual number,
the same table that belongs in the README's Benchmarks section.

Run with:
    python -m benchmarks.run_benchmarks
"""

import csv
import time
from typing import List, Optional

from algorithm_core.generator import generate_incompatible_pairs
from algorithm_core.graph_builder import build_compatibility_graph
from algorithm_core.cycle_finder import find_candidate_cycles
from algorithm_core.greedy_matcher import solve_greedy_matching

DEFAULT_POOL_SIZES = [50, 200, 1000, 2000]
SEED = 42


def _time_limit_for_pool(pool_size: int) -> float:
    """
    Larger pools produce more candidate cycles, which the ILP solver
    needs more time to search through. This scales the time budget
    with pool size instead of using one fixed limit for every run.
    """
    return min(60.0, max(5.0, pool_size / 20))


def run_single_benchmark(pool_size: int, seed: int = SEED) -> dict:
    """
    Generates one synthetic pool of the given size, runs both matchers
    against it, and returns a single row of benchmark data: how many
    patients each matcher matched, and how long each one took.
    """
    pairs = generate_incompatible_pairs(count=pool_size, seed=seed)
    graph = build_compatibility_graph(pairs, seed=seed)
    cycles = find_candidate_cycles(graph)

    # Imported here rather than at the top of the file, so that the
    # rest of this module (the table printing and CSV saving helpers)
    # can be imported and tested without OR-Tools installed.
    from algorithm_core.optimal_matcher import solve_optimal_matching

    time_limit = _time_limit_for_pool(pool_size)

    start = time.perf_counter()
    optimal_result = solve_optimal_matching(cycles, time_limit_seconds=time_limit)
    optimal_time_ms = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    greedy_result = solve_greedy_matching(cycles)
    greedy_time_ms = (time.perf_counter() - start) * 1000

    return {
        "pool_size": pool_size,
        "candidate_cycles": len(cycles),
        "optimal_matched": optimal_result.matched_pairs,
        "greedy_matched": greedy_result.matched_pairs,
        "optimal_time_ms": round(optimal_time_ms, 2),
        "greedy_time_ms": round(greedy_time_ms, 2),
        "solver_status": optimal_result.status,
    }


def run_all_benchmarks(pool_sizes: Optional[List[int]] = None) -> List[dict]:
    """Runs run_single_benchmark for every pool size and collects the results."""
    sizes = pool_sizes or DEFAULT_POOL_SIZES
    results = []
    for size in sizes:
        print(f"Running benchmark for pool size {size}...")
        results.append(run_single_benchmark(size))
    return results


def print_results_table(results: List[dict]) -> None:
    """Prints the benchmark results as a readable table, straight to the terminal."""
    header = (
        f"{'Pool':>6} | {'Cycles':>7} | {'Optimal':>8} | {'Greedy':>7} | "
        f"{'Opt time (ms)':>13} | {'Greedy time (ms)':>17}"
    )
    print("\n" + header)
    print("-" * len(header))
    for row in results:
        print(
            f"{row['pool_size']:>6} | {row['candidate_cycles']:>7} | "
            f"{row['optimal_matched']:>8} | {row['greedy_matched']:>7} | "
            f"{row['optimal_time_ms']:>13} | {row['greedy_time_ms']:>17}"
        )


def save_results_csv(results: List[dict], path: str = "benchmark_results.csv") -> None:
    """
    Saves the benchmark results to a CSV file, this is the file the
    README's Benchmarks table should eventually be filled in from.
    """
    if not results:
        return
    with open(path, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"\nSaved results to {path}")


def main():
    results = run_all_benchmarks()
    print_results_table(results)
    save_results_csv(results)


if __name__ == "__main__":
    main()
