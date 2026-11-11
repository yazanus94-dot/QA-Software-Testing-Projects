// Shared configuration: base URL and performance budgets (SLOs).
export const BASE_URL = __ENV.BASE_URL || 'https://jsonplaceholder.typicode.com';

// Budgets double as pass/fail criteria: k6 exits non-zero when a threshold is crossed.
export const thresholds = {
  http_req_failed: ['rate<0.01'],                 // < 1% errors
  http_req_duration: ['p(95)<800', 'p(99)<1500'], // latency budget in ms
  checks: ['rate>0.99'],                          // > 99% of checks pass
};
