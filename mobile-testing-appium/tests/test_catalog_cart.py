import pytest


@pytest.mark.smoke
def test_catalog_lists_products(catalog_page):
    assert catalog_page.is_loaded()
    titles = catalog_page.product_titles()
    assert len(titles) >= 2
    assert all(t.strip() for t in titles), "Every product must have a title"


@pytest.mark.smoke
def test_add_product_updates_cart_badge(catalog_page):
    catalog_page.open_first_product().add_current_product_to_cart()
    assert catalog_page.cart_count() == 1


@pytest.mark.regression
def test_cart_contains_added_product(catalog_page, cart_page):
    catalog_page.open_first_product().add_current_product_to_cart()
    catalog_page.open_cart()
    assert cart_page.is_loaded()
    assert len(cart_page.item_titles()) == 1


@pytest.mark.regression
def test_remove_item_empties_cart(catalog_page, cart_page):
    catalog_page.open_first_product().add_current_product_to_cart()
    catalog_page.open_cart()
    cart_page.remove_first_item()
    assert catalog_page.cart_count() == 0
