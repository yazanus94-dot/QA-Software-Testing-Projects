import { test, expect } from '../fixtures/test-fixtures';
import { users, PASSWORD } from '../test-data/users';

test.describe('Authentication', () => {
  test.beforeEach(async ({ loginPage }) => loginPage.goto());

  test('valid user can log in @smoke', async ({ loginPage, inventoryPage }) => {
    await loginPage.login(users.standard.username, users.standard.password);
    await inventoryPage.expectLoaded();
  });

  test('locked out user sees an error @smoke', async ({ loginPage }) => {
    await loginPage.login(users.locked.username, users.locked.password);
    await loginPage.expectError('this user has been locked out');
  });

  const invalid = [
    { name: 'wrong password', username: 'standard_user', password: 'nope', error: 'do not match' },
    { name: 'unknown user', username: 'ghost_user', password: PASSWORD, error: 'do not match' },
    { name: 'empty username', username: '', password: PASSWORD, error: 'Username is required' },
    { name: 'empty password', username: 'standard_user', password: '', error: 'Password is required' },
  ];
  for (const c of invalid) {
    test(`rejects ${c.name}`, async ({ loginPage }) => {
      await loginPage.login(c.username, c.password);
      await loginPage.expectError(c.error);
    });
  }

  test('protected page redirects anonymous users', async ({ page, loginPage }) => {
    await page.goto('/inventory.html');
    await loginPage.expectError("You can only access '/inventory.html' when you are logged in");
  });

  test('logout ends the session', async ({ loggedIn, page }) => {
    await loggedIn.logout();
    await expect(page).toHaveURL('/');
  });
});
