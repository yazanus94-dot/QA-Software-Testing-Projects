# Sample Bug Report

| Field | Value |
|---|---|
| **ID** | BUG-MOB-014 |
| **Title** | Cart badge keeps old count after removing the last item |
| **Severity / Priority** | Medium / Medium |
| **Environment** | Android 14 emulator (Pixel 6, API 34), My Demo App build 1.1, Appium 2.x |
| **Reported by** | YOUR NAME |
| **Status** | New |

### Preconditions
Logged-in user, empty cart.

### Steps to reproduce
1. Open the first product and tap **Add To Cart**.
2. Open the cart and tap **Remove item**.
3. Navigate back to the catalog.

### Expected result
Cart badge is hidden (count = 0).

### Actual result
Badge still shows `1` until the app is restarted.

### Evidence
`screenshots/test_remove_item_empties_cart_<time>.png` (captured automatically) · Appium log attached.

### Notes
Reproducible 3/3 times. Not reproducible when the cart is refreshed through pull-to-refresh. Suggested root cause: badge state not observing cart changes.

> *Illustrative example written for portfolio purposes; adjust to a real finding after you run the suite.*
