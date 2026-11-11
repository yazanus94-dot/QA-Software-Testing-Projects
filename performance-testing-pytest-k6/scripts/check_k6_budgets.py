"""Reads a k6 JSON summary (results/k6-*.json) and prints a compact budget table.

Usage: python scripts/check_k6_budgets.py results/k6-load.json [--p95 800] [--max-error-rate 0.01]
Exit code 1 when a budget is exceeded (handy as an extra CI gate / for portfolio screenshots).
"""
import argparse
import json
import sys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("summary")
    ap.add_argument("--p95", type=float, default=800)
    ap.add_argument("--max-error-rate", type=float, default=0.01)
    args = ap.parse_args()

    m = json.load(open(args.summary))["metrics"]

    def val(metric: str, key: str):
        """k6 summaries expose stats either flat or under a 'values' key depending on version."""
        d = m[metric]
        return d["values"][key] if "values" in d else d[key]

    p95 = val("http_req_duration", "p(95)")
    err = val("http_req_failed", "rate") if "values" in m["http_req_failed"] else m["http_req_failed"]["value"]
    reqs = val("http_reqs", "count")

    rows = [
        ("requests", reqs, "-", True),
        ("p95 latency (ms)", round(p95, 1), args.p95, p95 <= args.p95),
        ("error rate", round(err, 4), args.max_error_rate, err <= args.max_error_rate),
    ]
    print(f"{'metric':<20}{'value':>12}{'budget':>12}  status")
    for name, val, budget, ok in rows:
        print(f"{name:<20}{val:>12}{budget:>12}  {'PASS' if ok else 'FAIL'}")
    return 0 if all(r[3] for r in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
