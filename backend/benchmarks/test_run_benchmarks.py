import csv
import io
import os
import tempfile

from benchmarks.run_benchmarks import (
    print_results_table,
    save_results_csv,
    _time_limit_for_pool,
)


def test_time_limit_scales_with_pool_size():
    assert _time_limit_for_pool(50) == 5.0  # floor applies for small pools
    assert _time_limit_for_pool(2000) == 60.0  # ceiling applies for large pools
    assert _time_limit_for_pool(400) == 20.0  # normal scaling in between


def test_save_results_csv_writes_readable_rows():
    fake_results = [
        {
            "pool_size": 50,
            "candidate_cycles": 100,
            "optimal_matched": 40,
            "greedy_matched": 35,
            "optimal_time_ms": 120.5,
            "greedy_time_ms": 0.8,
            "solver_status": "OPTIMAL",
        }
    ]
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, "results.csv")
        save_results_csv(fake_results, path=path)

        with open(path, newline="") as csv_file:
            rows = list(csv.DictReader(csv_file))

        assert len(rows) == 1
        assert rows[0]["pool_size"] == "50"
        assert rows[0]["optimal_matched"] == "40"


def test_save_results_csv_does_nothing_for_empty_results():
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, "results.csv")
        save_results_csv([], path=path)
        assert not os.path.exists(path)


def test_print_results_table_runs_without_error(capsys):
    fake_results = [
        {
            "pool_size": 50,
            "candidate_cycles": 100,
            "optimal_matched": 40,
            "greedy_matched": 35,
            "optimal_time_ms": 120.5,
            "greedy_time_ms": 0.8,
        }
    ]
    print_results_table(fake_results)
    captured = capsys.readouterr()
    assert "Pool" in captured.out
    assert "50" in captured.out
