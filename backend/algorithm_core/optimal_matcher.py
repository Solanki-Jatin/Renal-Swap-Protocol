"""
Optimal cycle selection, using integer programming.

A single incompatible pair can only take part in one real swap. Given
every candidate exchange cycle found by cycle_finder, this module
decides which combination of non overlapping cycles maximizes the
total number of patients matched.

This selection step is exactly why the problem is NP-hard once cycles
longer than two are allowed, it is a constrained set packing problem,
not something a simple greedy pick can be trusted to solve optimally.
Real kidney exchange clearinghouses solve this with an integer
program, this module does the same, using Google OR-Tools' CP-SAT
solver, a constraint programming solver well suited to this kind of
binary decision problem.
"""

from typing import Dict, List, Tuple

from ortools.sat.python import cp_model

from .cycle_finder import cycle_value


class OptimalMatchResult:
    """Holds the outcome of a single optimal matching run."""

    def __init__(self, selected_cycles: List[Tuple[str, ...]], matched_pairs: int, status: str):
        self.selected_cycles = selected_cycles
        self.matched_pairs = matched_pairs
        self.status = status

    def to_dict(self) -> dict:
        return {
            "selected_cycles": [list(cycle) for cycle in self.selected_cycles],
            "matched_pairs": self.matched_pairs,
            "cycles_used": len(self.selected_cycles),
            "status": self.status,
        }


def solve_optimal_matching(
    candidate_cycles: List[Tuple[str, ...]],
    time_limit_seconds: float = 10.0,
) -> OptimalMatchResult:
    """
    Selects the set of vertex disjoint cycles that maximizes the total
    number of matched patients.

    Each candidate cycle becomes one binary decision variable: selected,
    or not. The only real constraint is that a given pair id cannot
    appear in more than one selected cycle, since a patient-donor pair
    can only take part in one actual swap. The objective maximizes the
    total number of patients matched across every selected cycle,
    which means a larger 3-way cycle can rightly outweigh a smaller
    2-way cycle it conflicts with.

    time_limit_seconds caps how long the solver searches. For the pool
    sizes this project targets, the solver should finish well within
    that, this is a safety net for larger stress test runs.
    """
    if not candidate_cycles:
        return OptimalMatchResult(selected_cycles=[], matched_pairs=0, status="NO_CANDIDATES")

    model = cp_model.CpModel()

    cycle_vars = [model.NewBoolVar(f"cycle_{i}") for i in range(len(candidate_cycles))]

    # Map each pair id to every candidate cycle index that includes it,
    # so a single "used at most once" constraint can be added per pair.
    pair_to_cycle_indices: Dict[str, List[int]] = {}
    for index, cycle in enumerate(candidate_cycles):
        for pair_id in cycle:
            pair_to_cycle_indices.setdefault(pair_id, []).append(index)

    for cycle_indices in pair_to_cycle_indices.values():
        model.Add(sum(cycle_vars[i] for i in cycle_indices) <= 1)

    objective_terms = [
        cycle_value(candidate_cycles[i]) * cycle_vars[i] for i in range(len(candidate_cycles))
    ]
    model.Maximize(sum(objective_terms))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_seconds
    status = solver.Solve(model)
    status_name = solver.StatusName(status)

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return OptimalMatchResult(selected_cycles=[], matched_pairs=0, status=status_name)

    selected_cycles = [
        candidate_cycles[i]
        for i in range(len(candidate_cycles))
        if solver.Value(cycle_vars[i]) == 1
    ]
    matched_pairs = sum(cycle_value(cycle) for cycle in selected_cycles)

    return OptimalMatchResult(
        selected_cycles=selected_cycles,
        matched_pairs=matched_pairs,
        status=status_name,
    )
