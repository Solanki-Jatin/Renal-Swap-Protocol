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

    print("\nNext up: cycle detection will turn this graph into actual matches.")


if __name__ == "__main__":
    main()
