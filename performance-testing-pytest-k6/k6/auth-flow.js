// Authenticated workflow under load: log in -> read a booking detail with the session token.
import http from 'k6/http';
import { check, sleep } from 'k6';
// Authenticated workflow targets Restful-Booker (JSONPlaceholder has no auth); override with RB_BASE_URL if needed.
const BASE_URL = __ENV.RB_BASE_URL || 'https://restful-booker.herokuapp.com';
import { makeSummary } from './lib/summary.js';

export const options = {
  vus: 5,
  duration: '1m',
  thresholds: { http_req_failed: ['rate<0.02'], 'http_req_duration{name:auth}': ['p(95)<1500'] },
};

const JSON_HEADERS = { headers: { 'Content-Type': 'application/json' } };

// Restful-Booker issues a session token for its fixed demo credentials.
export function setup() {
  const r = http.post(`${BASE_URL}/auth`,
    JSON.stringify({ username: 'admin', password: 'password123' }),
    { ...JSON_HEADERS, tags: { name: 'auth' } });
  check(r, { 'auth 200': (x) => x.status === 200, 'has token': (x) => !!x.json('token') });
  return { token: r.json('token') };
}

export default function (data) {
  const detail = http.get(`${BASE_URL}/booking/1`, { headers: { Cookie: `token=${data.token}` } });
  check(detail, {
    'booking detail 200': (r) => r.status === 200,
    'detail has firstname': (r) => !!r.json('firstname'),
  });
  sleep(1);
}

export const handleSummary = (data) => makeSummary('k6-auth-flow', data);
