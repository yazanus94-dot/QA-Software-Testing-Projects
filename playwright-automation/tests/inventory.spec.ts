import { test, expect } from '../fixtures/test-fixtures';

test.describe('Inventory', () => {
  test('sorts by name A→Z and Z→A', async ({ loggedIn }) => {
    await loggedIn.sortBy('az');
    const az = await loggedIn.productNames();
    expect(az).toEqual([...az].sort());

    await loggedIn.sortBy('za');
    const za = await loggedIn.productNames();
    expect(za).toEqual([...za].sort().reverse());
  });

  test('sorts by price low→high and high→low', async ({ loggedIn }) => {
    await loggedIn.sortBy('lohi');
    const asc = await loggedIn.productPrices();
    expect(asc).toEqual([...asc].sort((a, b) => a - b));

    await loggedIn.sortBy('hilo');
    const desc = await loggedIn.productPrices();
    expect(desc).toEqual([...desc].sort((a, b) => b - a));
  });

  test('every product has a name and a positive price', async ({ loggedIn }) => {
    for (const n of await loggedIn.productNames()) expect(n.trim()).not.toBe('');
    for (const p of await loggedIn.productPrices()) expect(p).toBeGreaterThan(0);
  });
});
