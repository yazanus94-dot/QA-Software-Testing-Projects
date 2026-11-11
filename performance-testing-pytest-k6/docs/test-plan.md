# Performance Test Plan

## Goals
Verify response time, throughput and error rate meet agreed budgets, find the capacity limit and confirm recovery after overload.

## Workload model
Read-heavy catalogue browsing (list → detail) with 1–3 s think time; 10% authenticated workflow.

## Targets (SLOs)
| Metric | Budget |
|---|---|
| p95 latency | < 800 ms |
| p99 latency | < 1500 ms |
| Error rate | < 1% (stress < 5%, spike < 10%) |
| Throughput (pytest gate) | ≥ 5 req/s |

## Test types
Smoke → Load → Stress → Spike → (optional) Soak 1–4 h.

## Environment
Same configuration as production where possible; k6 runs from a separate load generator (CI runner is for demo purposes only). Network latency of the runner is part of measured time.

## Monitoring
k6 metrics (`http_req_duration`, `http_req_failed`, `iterations`, custom Trend); in a real system add server CPU/memory, DB and queue metrics.

## Exit criteria
All thresholds green on load; stress test finds and documents the breaking point; system recovers within 2 minutes after spike.

## Risks
Shared public demo API may throttle (429) → lower VUs, check for 429 in results. CI runners add noise → compare trends, not single runs.
