"""HYBRID: create data through the API, verify it through the browser.

Target: Restful-Booker Platform demo (https://automationintesting.online).
Experimental - UI selectors may change; run manually:  pytest hybrid -m hybrid --headed
"""
import os
import uuid

import pytest
import requests
from playwright.sync_api import Page, expect

BASE = os.getenv("PLATFORM_URL", "https://automationintesting.online")
pytestmark = pytest.mark.hybrid


@pytest.fixture
def api_booking():
    lastname = f"QA{uuid.uuid4().hex[:6]}"
    body = {
        "roomid": 1, "firstname": "Hybrid", "lastname": lastname, "depositpaid": False,
        "email": "hybrid.test@example.com", "phone": "01234567890",
        "bookingdates": {"checkin": "2027-03-10", "checkout": "2027-03-12"},
    }
    r = requests.post(f"{BASE}/api/booking", json=body, timeout=20)
    assert r.status_code == 201, r.text
    yield {"lastname": lastname, "id": r.json().get("bookingid")}


def test_booking_created_by_api_is_visible_in_admin_ui(page: Page, api_booking):
    page.goto(f"{BASE}/#/admin")
    page.locator("#username").fill("admin")
    page.locator("#password").fill("password")
    page.locator("#doLogin").click()

    page.goto(f"{BASE}/#/admin/report")
    expect(page.get_by_text(api_booking["lastname"]).first).to_be_visible(timeout=15000)
