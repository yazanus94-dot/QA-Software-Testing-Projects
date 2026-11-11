# Test Cases & Traceability

| ID | Area | Scenario | Priority | Spec |
|---|---|---|---|---|
| WEB-001 | Auth | Valid login lands on inventory | High | login.spec.ts |
| WEB-002 | Auth | Locked-out user sees error | High | login.spec.ts |
| WEB-003 | Auth | Wrong password / unknown user rejected | High | login.spec.ts |
| WEB-004 | Auth | Empty username / password validation | Medium | login.spec.ts |
| WEB-005 | Auth | Anonymous access to /inventory.html is blocked | High | login.spec.ts |
| WEB-006 | Auth | Logout ends session | Medium | login.spec.ts |
| WEB-010 | Catalog | Sort by name A→Z / Z→A | Medium | inventory.spec.ts |
| WEB-011 | Catalog | Sort by price low→high / high→low | Medium | inventory.spec.ts |
| WEB-012 | Catalog | Every product has name and positive price | Low | inventory.spec.ts |
| WEB-020 | Cart | Badge reflects add/remove | High | cart-checkout.spec.ts |
| WEB-021 | Cart | Cart keeps selected items | High | cart-checkout.spec.ts |
| WEB-030 | Checkout | Complete E2E purchase | Critical | cart-checkout.spec.ts |
| WEB-031 | Checkout | Customer info required | Medium | cart-checkout.spec.ts |
| WEB-040 | Resilience | Page works when images are blocked | Low | network-resilience.spec.ts |
| WEB-041 | Resilience | No uncaught JS errors on inventory | Medium | network-resilience.spec.ts |
| WEB-050 | A11y | No critical WCAG A/AA violations on login | Medium | a11y-visual.spec.ts |
| WEB-051 | Visual | Login page matches baseline | Low | a11y-visual.spec.ts |
