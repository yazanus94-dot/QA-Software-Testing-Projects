import { htmlReport } from 'https://raw.githubusercontent.com/benc-uk/k6-reporter/2.2.0/dist/bundle.js';
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.0.2/index.js';

// Writes an HTML report + JSON summary to results/ and prints a text summary.
export function makeSummary(name, data) {
  return {
    stdout: textSummary(data, { indent: ' ', enableColors: true }),
    [`results/${name}.html`]: htmlReport(data),
    [`results/${name}.json`]: JSON.stringify(data, null, 2),
  };
}
