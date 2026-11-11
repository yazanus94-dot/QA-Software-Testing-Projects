"""Pytest-driven performance checks: same budgets, asserted like any other test.

Why both pytest and k6?
  * pytest  -> quick budget gates inside the normal test run / PR pipeline, easy to extend in Python
  * k6      -> realistic multi-stage load profiles (load, stress, spike) with rich metrics
"""
import pytest

from pytest_perf.perf_utils import percentile, run_load


def test_percentile_helper_is_correct():
    data = sorted(range(1, 101))
    assert percentile(data, 50) == 50
    assert percentile(data, 95) == 95
    assert percentile(data, 100) == 100


@pytest.mark.smoke
def test_single_request_is_fast(base_url, budgets):
    r = run_load("single", f"{base_url}/public/crocodiles/", total_requests=1, concurrency=1)
    assert r.errors == 0
    assert r.max_ms < budgets["p99_ms"]


@pytest.mark.load
@pytest.mark.parametrize("users", [5, 20])
def test_list_endpoint_meets_budget_under_concurrency(base_url, budgets, users):
    r = run_load(f"list-{users}vu", f"{base_url}/public/crocodiles/", total_requests=users * 10, concurrency=users)
    assert r.error_rate <= budgets["error_rate"], f"error rate {r.error_rate:.2%}"
    assert r.p95_ms <= budgets["p95_ms"], f"p95 {r.p95_ms} ms over budget"
    assert r.p99_ms <= budgets["p99_ms"], f"p99 {r.p99_ms} ms over budget"
    assert r.rps >= budgets["min_rps"], f"throughput {r.rps} rps below minimum"


@pytest.mark.load
def test_detail_endpoint_latency(base_url, budgets):
    r = run_load("detail", f"{base_url}/public/crocodiles/1/", total_requests=60, concurrency=10)
    assert r.error_rate <= budgets["error_rate"]
    assert r.p95_ms <= budgets["p95_ms"]


@pytest.mark.load
def test_latency_does_not_degrade_with_more_users(base_url):
    """Scalability sanity check: 4x the concurrency must not make p95 worse than 4x."""
    low = run_load("scale-low", f"{base_url}/public/crocodiles/", total_requests=40, concurrency=5)
    high = run_load("scale-high", f"{base_url}/public/crocodiles/", total_requests=160, concurrency=20)
    assert high.p95_ms <= max(low.p95_ms * 4, 300), f"p95 grew from {low.p95_ms} to {high.p95_ms} ms"
