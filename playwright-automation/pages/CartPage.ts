import { Page, Locator, expect } from '@playwright/test';

export class CartPage {
  readonly items: Locator;
  readonly checkoutButton: Locator;

  constructor(private readonly page: Page) {
    this.items = page.getByTestId('inventory-item');
    this.checkoutButton = page.getByTestId('checkout');
  }

  async expectItemCount(n: number) {
    await expect(this.items).toHaveCount(n);
  }

  async remove(slug: string) {
    await this.page.getByTestId(`remove-${slug}`).click();
  }

  async checkout() {
    await this.checkoutButton.click();
  }
}
