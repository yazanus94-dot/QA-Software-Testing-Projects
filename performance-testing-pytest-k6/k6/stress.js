// STRESS: push beyond normal load to find the breaking point and watch recovery.
import http from 'k6/http';
import { check, sleep } from 'k6';
import { BASE_URL } from './lib/config.js';
import { makeSummary } from './lib/summary.js';

export const options = {
  stages: [
    { duration: '1m', target: 20 },
    { duration: '2m', target: 50 },
    { duration: '2m', target: 100 },
    { duration: '1m', target: 0 },   // recovery
  ],
  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<2000'],
  },
  tags: { test_type: 'stress' },
};

export default function () {
  const res = http.get(`${BASE_URL}/posts`);
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}

export const handleSummary = (data) => makeSummary('k6-stress', data);
