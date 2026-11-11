"""Self-healing demo. Runs fully offline (HTML is injected with page.set_content)."""
import pytest

pytest.importorskip("playwright.sync_api", reason="pip install playwright && playwright install chromium")
from playwright.sync_api import sync_playwright  # noqa: E402

from ai_tools.self_healing.healing_locator import HealingLocator  # noqa: E402

pytestmark = pytest.mark.ai_tools

# 'Version 2' of the page: developers renamed the id and the CSS class of the button.
PAGE_V2 = """
<form>
  <input data-test="username" placeholder="Username"/>
  <button id="btn-signin-v2" class="primary-v2" type="submit">Log in</button>
</form>
"""


@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page()
        yield pg
        browser.close()


def test_locator_heals_when_id_changes(page):
    page.set_content(PAGE_V2)
    healer = HealingLocator(page)

    button = healer.find(
        "login button",
        primary="#login-button",  # BROKEN: this id no longer exists
        fallbacks=[
            ("role+name", page.get_by_role("button", name="Log in")),
            ("css attribute", "button[type=submit]"),
        ],
    )
    button.click()  # test keeps running

    assert len(healer.log.events) == 1
    assert healer.log.events[0].strategy == "role+name"
    healer.log.save()


def test_no_healing_needed_when_primary_works(page):
    page.set_content(PAGE_V2)
    healer = HealingLocator(page)
    healer.find("username", primary="[data-test=username]", fallbacks=[])
    assert healer.log.events == []


def test_ambiguous_fallback_is_not_trusted(page):
    page.set_content("<button>Log in</button><button>Log in</button>")
    healer = HealingLocator(page)
    with pytest.raises(AssertionError):
        healer.find("login", "#gone", [("role+name", page.get_by_role("button", name="Log in"))])


def test_healing_never_masks_a_real_defect(page):
    """If the element is truly gone, the test must FAIL - healing is not a way to hide bugs."""
    page.set_content("<p>Page crashed</p>")
    healer = HealingLocator(page)
    with pytest.raises(AssertionError):
        healer.find("login", "#login-button", [("role+name", page.get_by_role("button", name="Log in"))])
