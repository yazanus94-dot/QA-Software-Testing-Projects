# Test Cases

| ID | Title | Preconditions | Steps | Expected result | Type | Automated |
|---|---|---|---|---|---|---|
| MOB-001 | Valid login | App installed, fresh launch | Menu → Log in → enter valid credentials → tap Login | Product catalog is displayed | Smoke | `test_valid_login_shows_catalog` |
| MOB-002 | Unknown user rejected | Login screen open | Enter unknown email + any password | Login rejected, catalog not shown | Negative | `test_invalid_login_is_rejected[unknown-user]` |
| MOB-003 | Wrong password rejected | Login screen open | Valid email + wrong password | Login rejected | Negative | `[wrong-password]` |
| MOB-004 | Empty fields | Login screen open | Tap Login with empty fields | Login rejected | Boundary | `[empty-fields]` |
| MOB-005 | Locked-out user | Login screen open | Login as locked user | "locked out" error shown | Negative | `test_locked_out_user_sees_error` |
| MOB-006 | Logout | Logged in | Menu → Log out | Returned to unauthenticated state | Regression | `test_logout_returns_to_login` |
| MOB-007 | Catalog lists products | App launched | Open catalog | ≥2 products, each with a title | Smoke | `test_catalog_lists_products` |
| MOB-008 | Add to cart updates badge | Catalog open | Open product → Add to cart | Cart badge shows 1 | Smoke | `test_add_product_updates_cart_badge` |
| MOB-009 | Cart shows added item | Item added | Open cart | Exactly 1 line item | Regression | `test_cart_contains_added_product` |
| MOB-010 | Remove item | Item in cart | Tap remove | Cart is empty, badge cleared | Regression | `test_remove_item_empties_cart` |
| MOB-011 | Scroll reveals products | Catalog open | Scroll down | New products become visible | Gesture | `test_scroll_reveals_more_products` |
| MOB-012 | Rotation | Catalog open | Rotate to landscape | Catalog still rendered | Device | `test_orientation_change_keeps_state` |
| MOB-013 | Background/resume | Catalog open | Background 3 s, resume | Same screen restored | Device | `test_app_survives_background_and_resume` |
