# Sample Performance Defect Report

| Field | Value |
|---|---|
| **ID** | PERF-BUG-003 |
| **Title** | p95 latency of `GET /public/crocodiles/` exceeds budget at 100 concurrent users |
| **Severity / Priority** | High / High |
| **Environment** | k6 0.5x on GitHub-hosted runner, target `test-api.k6.io` |
| **Reported by** | YOUR NAME |

### Scenario
`k6 run k6/stress.js` (ramp to 100 VUs).

### Expected
p95 < 2000 ms, error rate < 5%.

### Observed *(fill in from your run — values below are placeholders)*
p95 = `<value>` ms, p99 = `<value>` ms, error rate = `<value>` %, degradation begins near `<N>` VUs.

### Evidence
`results/k6-stress.html`, `results/k6-stress.json`

### Suggested investigation
Check server CPU/DB connections at the degradation point, caching of the list endpoint, connection-pool limits, rate limiting.

> *Template for reporting a real finding after you run the stress test; replace the placeholders with your numbers.*
