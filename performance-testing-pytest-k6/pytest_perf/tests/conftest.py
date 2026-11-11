import os

import pytest


@pytest.fixture(scope="session")
def base_url() -> str:
    # JSONPlaceholder: a stable public JSON API suited to latency budget gates.
    # (Restful-Booker, the auth-flow target, rate-limits bursts on its free dyno.)
    return os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com").rstrip("/")


# Performance budgets (override via env to tighten/relax per environment).
@pytest.fixture(scope="session")
def budgets() -> dict:
    return {
        "p95_ms": float(os.getenv("BUDGET_P95_MS", "1000")),
        "p99_ms": float(os.getenv("BUDGET_P99_MS", "2000")),
        "error_rate": float(os.getenv("BUDGET_ERROR_RATE", "0.01")),
        "min_rps": float(os.getenv("BUDGET_MIN_RPS", "5")),
    }
