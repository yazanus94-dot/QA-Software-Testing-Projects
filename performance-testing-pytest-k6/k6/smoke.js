// SMOKE: 1 VU, 30s. "Does the system work at all under minimal load?"
import http from 'k6/http';
import { check, sleep } from 'k6';
import { BASE_URL, thresholds } from './lib/config.js';
import { makeSummary } from './lib/summary.js';

export const options = { vus: 1, duration: '30s', thresholds, tags: { test_type: 'smoke' } };

export default function () {
  const res = http.get(`${BASE_URL}/posts`);
  check(res, {
    'status is 200': (r) => r.status === 200,
    'returns a list': (r) => Array.isArray(r.json()),
    'list is not empty': (r) => r.json().length > 0,
  });
  sleep(1);
}

export const handleSummary = (data) => makeSummary('k6-smoke', data);
