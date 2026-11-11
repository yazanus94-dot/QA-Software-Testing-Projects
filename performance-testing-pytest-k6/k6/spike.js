// SPIKE: sudden surge (e.g. marketing campaign) then immediate drop.
import http from 'k6/http';
import { check, sleep } from 'k6';
import { BASE_URL } from './lib/config.js';
import { makeSummary } from './lib/summary.js';

export const options = {
  stages: [
    { duration: '20s', target: 5 },
    { duration: '10s', target: 150 },  // spike
    { duration: '1m', target: 150 },
    { duration: '10s', target: 5 },    // drop
    { duration: '30s', target: 5 },    // recovery observation
    { duration: '10s', target: 0 },
  ],
  thresholds: { http_req_failed: ['rate<0.10'], http_req_duration: ['p(95)<3000'] },
  tags: { test_type: 'spike' },
};

export default function () {
  const res = http.get(`${BASE_URL}/public/crocodiles/`);
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}

export const handleSummary = (data) => makeSummary('k6-spike', data);
