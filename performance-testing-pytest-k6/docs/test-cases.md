# Performance Test Cases

| ID | Type | Tool | Scenario | Pass criteria |
|---|---|---|---|---|
| PERF-001 | Smoke | k6 | 1 VU for 30 s on `/public/crocodiles/` | 100% checks, p95 < 800 ms |
| PERF-002 | Load | k6 | 20 VUs, list → detail journey, 5 min | p95 < 800 ms, errors < 1%, detail p95 < 700 ms |
| PERF-003 | Stress | k6 | Ramp 20 → 100 VUs | errors < 5%, p95 < 2 s, recovery after ramp-down |
| PERF-004 | Spike | k6 | 5 → 150 VUs in 10 s | errors < 10%, p95 < 3 s |
| PERF-005 | Workflow | k6 | Register → login → authenticated call, 5 VUs | login p95 < 1.5 s |
| PERF-010 | Budget gate | pytest | 50 requests, 5 threads | error ≤ 1%, p95 ≤ 1 s, rps ≥ 5 |
| PERF-011 | Budget gate | pytest | 200 requests, 20 threads | same budgets |
| PERF-012 | Detail endpoint | pytest | 60 requests, 10 threads | p95 ≤ 1 s |
| PERF-013 | Scalability | pytest | 5 vs 20 concurrent users | p95 grows less than 4× |
| PERF-014 | Unit | pytest | Percentile helper correctness | exact values |
