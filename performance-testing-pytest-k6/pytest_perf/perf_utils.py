"""Small, dependency-light load helper for pytest-based performance checks."""
import json
import math
import statistics
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from pathlib import Path

import requests

RESULTS = Path(__file__).resolve().parent.parent / "results"


@dataclass
class LoadResult:
    name: str
    requests: int
    errors: int
    duration_s: float
    rps: float
    avg_ms: float
    p50_ms: float
    p90_ms: float
    p95_ms: float
    p99_ms: float
    max_ms: float

    @property
    def error_rate(self) -> float:
        return self.errors / self.requests if self.requests else 1.0


def percentile(sorted_values: list[float], pct: float) -> float:
    """Nearest-rank percentile on an already sorted list."""
    if not sorted_values:
        return 0.0
    rank = math.ceil(pct / 100 * len(sorted_values))
    return sorted_values[max(0, min(len(sorted_values) - 1, rank - 1))]


def _one(session: requests.Session, method: str, url: str, retries: int = 1, **kw):
    start = time.perf_counter()
    for attempt in range(retries + 1):
        try:
            r = session.request(method, url, timeout=15, **kw)
            ok = r.status_code < 400
        except requests.RequestException:
            ok = False
        if ok or attempt == retries:
            break
        time.sleep(1.0)
    return (time.perf_counter() - start) * 1000, ok


def run_load(name: str, url: str, total_requests: int = 100, concurrency: int = 10, method: str = "GET", **kw) -> LoadResult:
    """Fire `total_requests` at `url` using `concurrency` worker threads and aggregate latency stats."""
    started = time.perf_counter()
    with requests.Session() as session, ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = [pool.submit(_one, session, method, url, **kw) for _ in range(total_requests)]
        samples = [f.result() for f in futures]
    elapsed = time.perf_counter() - started

    latencies = sorted(ms for ms, _ in samples)
    errors = sum(1 for _, ok in samples if not ok)
    result = LoadResult(
        name=name, requests=total_requests, errors=errors, duration_s=round(elapsed, 2),
        rps=round(total_requests / elapsed, 2), avg_ms=round(statistics.fmean(latencies), 1),
        p50_ms=round(percentile(latencies, 50), 1), p90_ms=round(percentile(latencies, 90), 1),
        p95_ms=round(percentile(latencies, 95), 1), p99_ms=round(percentile(latencies, 99), 1),
        max_ms=round(latencies[-1], 1),
    )
    save_result(result)
    return result


def save_result(result: LoadResult) -> None:
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / f"pytest-{result.name}.json").write_text(json.dumps(asdict(result), indent=2))
