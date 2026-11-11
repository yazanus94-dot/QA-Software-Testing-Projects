# ⚡ Performance Testing — k6 + Pytest

![k6](https://img.shields.io/badge/k6-load_testing-7D64FF) ![Pytest](https://img.shields.io/badge/Pytest-budget_gates-green) ![CI](https://img.shields.io/badge/GitHub_Actions-ready-black)

Two complementary approaches to performance testing, both with **explicit performance budgets (SLOs)**:

| Tool | Use it for | Files |
|---|---|---|
| **k6** | Realistic load profiles: smoke, load, stress, spike, authenticated workflow; HTML + JSON reports | `k6/` |
| **pytest** | Fast latency/throughput budget gates in the normal test run, custom Python logic | `pytest_perf/` |

Targets: the public [JSONPlaceholder](https://jsonplaceholder.typicode.com) API for list/detail latency profiles, and [Restful-Booker](https://restful-booker.herokuapp.com/apidoc/index.html) for the authenticated workflow (both are public demo/test APIs made for this purpose).

> Author: **Yazan Aljabari** | QA / Software Test Engineer

## Test types
| Script | Profile | Question answered |
|---|---|---|
| `smoke.js` | 1 VU · 30 s | Does it work at all? |
| `load.js` | ramp to 20 VUs, hold 3 min | Does it meet SLOs at expected traffic? (user journey + custom metric) |
| `stress.js` | up to 100 VUs | Where does it start to degrade? Does it recover? |
| `spike.js` | sudden jump to 150 VUs | How does it handle a sudden surge? |
| `auth-flow.js` | register → login → authenticated call | Multi-step workflow under load |
| `pytest_perf/` | 5–20 concurrent threads | Are p95/p99, error rate and RPS within budget? |

**Budgets (thresholds):** error rate < 1% · p95 < 800 ms · p99 < 1500 ms · checks > 99%.

## Run
```bash
# k6 (install: https://k6.io/docs/get-started/installation/)
k6 run k6/smoke.js
k6 run k6/load.js
k6 run -e BASE_URL=https://staging.example.com k6/load.js
# reports are written to results/k6-*.html and results/k6-*.json

# pytest
pip install -r requirements.txt
pytest                        # all
pytest -m smoke               # one request sanity
BUDGET_P95_MS=500 pytest -m load   # tighten the budget
# report: results/pytest-report.html

# budget table from a k6 JSON summary
python scripts/check_k6_budgets.py results/k6-load.json --p95 800
```

## How to read the results
* **p95/p99** matter more than the average: they show what the slowest users experience.
* A failing **threshold** makes k6 exit non-zero → the CI job fails (performance regression gate).
* Compare runs over time; run the same profile before and after a change.

## Structure
```
k6/            scripts + shared config/summary helpers
pytest_perf/   load helper (threads) + budget tests
scripts/       k6 budget checker
docs/          test plan, test cases, sample bug report
```
> Be considerate: only run load tests against systems you own or that explicitly allow it (the k6 demo API does).
