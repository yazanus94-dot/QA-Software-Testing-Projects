import AxeBuilder from '@axe-core/playwright';
import { test, expect } from '../fixtures/test-fixtures';

test.describe('Accessibility audit (report-only)', () => {
  test('login page: axe scan attached to the report', async ({ page, loginPage }, testInfo) => {
    await loginPage.goto();
    const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa']).analyze();
    await testInfo.attach('axe-results', {
      body: JSON.stringify(results.violations, null, 2),
      contentType: 'application/json',
    });
    // Report-only on a public demo site: fail just on *critical* issues.
    const critical = results.violations.filter((v) => v.impact === 'critical');
    expect(critical, `Critical a11y violations: ${critical.map((v) => v.id).join(', ')}`).toEqual([]);
  });
});

test.describe('Visual regression @visual', () => {
  test('login page screenshot', async ({ page, loginPage }) => {
    await loginPage.goto();
    await expect(page).toHaveScreenshot('login.png', { maxDiffPixelRatio: 0.02 });
  });
});
