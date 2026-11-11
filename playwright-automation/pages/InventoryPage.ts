import { Page, Locator, expect } from '@playwright/test';

export type SortOption = 'az' | 'za' | 'lohi' | 'hilo';

export class InventoryPage {
  readonly items: Locator;
  readonly names: Locator;
  readonly prices: Locator;
  readonly sort: Locator;
  readonly cartLink: Locator;
  readonly cartBadge: Locator;

  constructor(private readonly page: Page) {
    this.items = page.getByTestId('inventory-item');
    this.names = page.getByTestId('inventory-item-name');
    this.prices = page.getByTestId('inventory-item-price');
    this.sort = page.getByTestId('product-sort-container');
    this.cartLink = page.getByTestId('shopping-cart-link');
    this.cartBadge = page.getByTestId('shopping-cart-badge');
  }

  async expectLoaded() {
    await expect(this.page).toHaveURL(/inventory\.html/);
    await expect(this.items).toHaveCount(6);
  }

  async sortBy(option: SortOption) {
    await this.sort.selectOption(option);
  }

  async addToCart(slug: string) {
    await this.page.getByTestId(`add-to-cart-${slug}`).click();
  }

  async removeFromCart(slug: string) {
    await this.page.getByTestId(`remove-${slug}`).click();
  }

  async productNames(): Promise<string[]> {
    return this.names.allInnerTexts();
  }

  async productPrices(): Promise<number[]> {
    const raw = await this.prices.allInnerTexts();
    return raw.map((p) => Number(p.replace('$', '')));
  }

  async openCart() {
    await this.cartLink.click();
  }

  async logout() {
    await this.page.getByRole('button', { name: 'Open Menu' }).click();
    await this.page.getByTestId('logout-sidebar-link').click();
  }
}
