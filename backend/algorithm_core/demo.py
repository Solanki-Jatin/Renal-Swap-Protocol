"""
Quick end to end demo of the algorithm core, runnable straight from the
terminal, with no web server or frontend involved.

Run with:
    python -m algorithm_core.demo
"""

from algorithm_core.generator import generate_incompatible_pairs, generate_altruistic_donors
from algorithm_core.graph_builder import build_compatibility_graph, graph_summary
from algorithm_core.cycle_finder import find_candidate_cycles, cycles_summary
from algorithm_core.optimal_matcher import solve_optimal_matching
from algorithm_core.greedy_matcher import solve_greedy_matching


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

    print("\nSolving with the optimal ILP matcher...")
    optimal_result = solve_optimal_matching(cycles)
    print(f"  solver status: {optimal_result.status}")
    print(f"  cycles selected: {len(optimal_result.selected_cycles)}")
    print(f"  total patients matched: {optimal_result.matched_pairs}")

    print("\nSolving with the greedy baseline matcher...")
    greedy_result = solve_greedy_matching(cycles)
    print(f"  cycles selected: {len(greedy_result.selected_cycles)}")
    print(f"  total patients matched: {greedy_result.matched_pairs}")

    print(f"\nOut of {len(pairs)} pairs in the pool:")
    print(f"  optimal matched {optimal_result.matched_pairs} patients")
    print(f"  greedy matched {greedy_result.matched_pairs} patients")

    if optimal_result.matched_pairs > greedy_result.matched_pairs:
        gap = optimal_result.matched_pairs - greedy_result.matched_pairs
        print(f"  optimal found {gap} more matches than greedy on this pool")

    print(
        "\nNext up: a formal benchmark suite, running both matchers "
        "across many pool sizes and recording match rate and runtime."
    )


if __name__ == "__main__":
    main()
