import { Page, expect } from '@playwright/test';

export class CheckoutPage {
  constructor(private readonly page: Page) {}

  async fillInformation(info: { firstName: string; lastName: string; postalCode: string }) {
    await this.page.getByTestId('firstName').fill(info.firstName);
    await this.page.getByTestId('lastName').fill(info.lastName);
    await this.page.getByTestId('postalCode').fill(info.postalCode);
    await this.page.getByTestId('continue').click();
  }

  async expectOverviewTotal() {
    await expect(this.page.getByTestId('total-label')).toContainText('Total: $');
  }

  async finish() {
    await this.page.getByTestId('finish').click();
  }

  async expectOrderComplete() {
    await expect(this.page.getByTestId('complete-header')).toHaveText('Thank you for your order!');
  }

  async expectValidationError(text: string | RegExp) {
    await expect(this.page.getByTestId('error')).toContainText(text);
  }
}
