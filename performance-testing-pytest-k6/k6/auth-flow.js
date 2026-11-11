// API workflow under load: register -> login -> authenticated request (setup creates the user once).
import http from 'k6/http';
import { check, sleep } from 'k6';
import { BASE_URL } from './lib/config.js';
import { makeSummary } from './lib/summary.js';

export const options = {
  vus: 5,
  duration: '1m',
  thresholds: { http_req_failed: ['rate<0.02'], 'http_req_duration{name:login}': ['p(95)<1500'] },
};

const JSON_HEADERS = { headers: { 'Content-Type': 'application/json' } };

export function setup() {
  const user = `qa_${Date.now()}_${Math.floor(Math.random() * 1e6)}`;
  const creds = { username: user, password: 'S3cret-pass!', email: `${user}@example.com`, first_name: 'QA', last_name: 'Perf' };
  const r = http.post(`${BASE_URL}/user/register/`, JSON.stringify(creds), JSON_HEADERS);
  check(r, { 'registered (201)': (x) => x.status === 201 });
  return creds;
}

export default function (creds) {
  const login = http.post(`${BASE_URL}/auth/token/login/`,
    JSON.stringify({ username: creds.username, password: creds.password }),
    { ...JSON_HEADERS, tags: { name: 'login' } });
  const ok = check(login, { 'login 200': (r) => r.status === 200, 'has token': (r) => !!r.json('access') });
  if (!ok) return;

  const mine = http.get(`${BASE_URL}/my/crocodiles/`, { headers: { Authorization: `Bearer ${login.json('access')}` } });
  check(mine, { 'my crocodiles 200': (r) => r.status === 200 });
  sleep(1);
}

export const handleSummary = (data) => makeSummary('k6-auth-flow', data);
