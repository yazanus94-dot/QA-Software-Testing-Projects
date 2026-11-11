import pytest

from config import settings


@pytest.mark.smoke
def test_valid_login_shows_catalog(login_page, catalog_page):
    login_page.open_login().login(**settings.VALID_USER)
    assert catalog_page.is_loaded(), "Catalog should be visible after a valid login"


@pytest.mark.regression
@pytest.mark.parametrize(
    "email,password",
    [
        ("wrong@example.com", "badpass"),
        (settings.VALID_USER["email"], "wrong-password"),
        ("", ""),
    ],
    ids=["unknown-user", "wrong-password", "empty-fields"],
)
def test_invalid_login_is_rejected(login_page, catalog_page, email, password):
    login_page.open_login().login(email, password)
    assert not catalog_page.is_loaded(), "Catalog must NOT load with invalid credentials"


@pytest.mark.regression
def test_locked_out_user_sees_error(login_page):
    login_page.open_login().login(**settings.LOCKED_USER)
    assert "locked out" in login_page.error_message().lower()


@pytest.mark.regression
def test_logout_returns_to_login(login_page, catalog_page):
    login_page.open_login().login(**settings.VALID_USER)
    assert catalog_page.is_loaded()
    login_page.logout()
    assert login_page.is_visible(login_page.MENU_BUTTON)
