"""
Quick end to end demo of the algorithm core, runnable straight from the
terminal, with no web server or frontend involved. This is the fastest
way to prove the core algorithm actually works.

As later phases (cycle detection, optimal and greedy matching) get
built, this script will grow to show the full pipeline. Right now it
covers dataset generation and the compatibility graph.

Run with:
    python -m algorithm_core.demo
"""

from algorithm_core.generator import generate_incompatible_pairs, generate_altruistic_donors
from algorithm_core.graph_builder import build_compatibility_graph, graph_summary
from algorithm_core.cycle_finder import find_candidate_cycles, cycles_summary
from algorithm_core.optimal_matcher import solve_optimal_matching


def main():
    print("Generating a synthetic pool of incompatible patient-donor pairs...")
    pairs = generate_incompatible_pairs(
        count=30,
        hospital_ids=["hospital-A", "hospital-B"],
        seed=42,
    )
    print(f"Generated {len(pairs)} incompatible pairs.\n")

    altruistic_donors = generate_altruistic_donors(count=2, seed=42)
    print(f"Generated {len(altruistic_donors)} altruistic donors.\n")

    print("Building the compatibility graph...")
    graph = build_compatibility_graph(pairs, seed=42)
    summary = graph_summary(graph)

    print("\nGraph summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")

    print("\nSearching for valid 2-way and 3-way exchange cycles...")
    cycles = find_candidate_cycles(graph)
    cycle_stats = cycles_summary(cycles)

    print("\nCandidate cycles found:")
    for key, value in cycle_stats.items():
        print(f"  {key}: {value}")

    if cycles:
        print("\nExample cycle (a valid, ready to happen swap):")
        print(f"  {cycles[0]}")

    print("\nSolving for the optimal, non-overlapping combination of cycles...")
    result = solve_optimal_matching(cycles)
    print(f"  solver status: {result.status}")
    print(f"  cycles selected: {len(result.selected_cycles)}")
    print(f"  total patients matched: {result.matched_pairs} out of {len(pairs)} pairs in the pool")

    print(
        "\nNext up: a fast greedy baseline, so the optimal result above "
        "can be compared against it on both match rate and runtime."
    )


if __name__ == "__main__":
    main()
