// LOAD: ramp to expected production traffic, hold, ramp down. Includes a realistic user journey.
import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Trend } from 'k6/metrics';
import { BASE_URL, thresholds } from './lib/config.js';
import { makeSummary } from './lib/summary.js';

const detailLatency = new Trend('crocodile_detail_duration', true);

export const options = {
  stages: [
    { duration: '1m', target: 20 },  // ramp up
    { duration: '3m', target: 20 },  // steady state
    { duration: '30s', target: 0 },  // ramp down
  ],
  thresholds: { ...thresholds, crocodile_detail_duration: ['p(95)<700'] },
  tags: { test_type: 'load' },
};

export default function () {
  group('browse catalogue', () => {
    const list = http.get(`${BASE_URL}/public/crocodiles/`);
    check(list, { 'list 200': (r) => r.status === 200 });

    const items = list.json();
    const pick = items[Math.floor(Math.random() * items.length)];

    const detail = http.get(`${BASE_URL}/public/crocodiles/${pick.id}/`);
    detailLatency.add(detail.timings.duration);
    check(detail, {
      'detail 200': (r) => r.status === 200,
      'detail has name': (r) => !!r.json('name'),
    });
  });
  sleep(Math.random() * 2 + 1); // think time 1-3 s
}

export const handleSummary = (data) => makeSummary('k6-load', data);
