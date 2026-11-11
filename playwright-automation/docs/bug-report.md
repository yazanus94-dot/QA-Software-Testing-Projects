# Sample Bug Report

| Field | Value |
|---|---|
| **ID** | BUG-WEB-007 |
| **Title** | `problem_user` sees the same product image for every item |
| **Severity / Priority** | Medium / Medium |
| **Environment** | Chromium 130, Windows 11, https://www.saucedemo.com |
| **Reported by** | YOUR NAME |

### Steps to reproduce
1. Open the site and log in as `problem_user` / `secret_sauce`.
2. Look at the product images on the inventory page.

### Expected result
Each product shows its own image.

### Actual result
All products display the same image.

### Evidence
Playwright trace (`trace.zip`) and screenshot attached from the failing run.

### Automation note
Add an assertion comparing `img[src]` values for uniqueness to `inventory.spec.ts` when running as `problem_user`.

> *Known behaviour of the demo user, used here as a realistic example for portfolio purposes.*
