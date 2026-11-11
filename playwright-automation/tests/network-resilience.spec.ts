import { test, expect } from '../fixtures/test-fixtures';

test.describe('Network control (page.route)', () => {
  test('page remains usable when images fail to load', async ({ page, loggedIn }) => {
    await page.route('**/*.{png,jpg,jpeg,svg}', (route) => route.abort());
    await page.reload();
    await expect(loggedIn.items).toHaveCount(6);
  });

  test('no console errors on the inventory page', async ({ page, loggedIn }) => {
    const errors: string[] = [];
    page.on('pageerror', (e) => errors.push(e.message));
    await page.reload();
    await expect(loggedIn.items).toHaveCount(6);
    expect(errors).toEqual([]);
  });
});
