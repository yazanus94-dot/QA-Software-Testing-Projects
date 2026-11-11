import { test, expect } from '../fixtures/test-fixtures';
import { checkoutInfo } from '../test-data/users';

const BACKPACK = 'sauce-labs-backpack';
const BIKE_LIGHT = 'sauce-labs-bike-light';

test.describe('Cart & checkout', () => {
  test('add and remove items updates the badge', async ({ loggedIn }) => {
    await loggedIn.addToCart(BACKPACK);
    await loggedIn.addToCart(BIKE_LIGHT);
    await expect(loggedIn.cartBadge).toHaveText('2');
    await loggedIn.removeFromCart(BACKPACK);
    await expect(loggedIn.cartBadge).toHaveText('1');
  });

  test('cart keeps selected items @smoke', async ({ loggedIn, cartPage }) => {
    await loggedIn.addToCart(BACKPACK);
    await loggedIn.openCart();
    await cartPage.expectItemCount(1);
  });

  test('complete end-to-end purchase @smoke', async ({ loggedIn, cartPage, checkoutPage }) => {
    await loggedIn.addToCart(BACKPACK);
    await loggedIn.addToCart(BIKE_LIGHT);
    await loggedIn.openCart();
    await cartPage.expectItemCount(2);
    await cartPage.checkout();
    await checkoutPage.fillInformation(checkoutInfo);
    await checkoutPage.expectOverviewTotal();
    await checkoutPage.finish();
    await checkoutPage.expectOrderComplete();
  });

  test('checkout requires customer information', async ({ loggedIn, cartPage, checkoutPage }) => {
    await loggedIn.addToCart(BACKPACK);
    await loggedIn.openCart();
    await cartPage.checkout();
    await checkoutPage.fillInformation({ firstName: '', lastName: '', postalCode: '' });
    await checkoutPage.expectValidationError('First Name is required');
  });
});
