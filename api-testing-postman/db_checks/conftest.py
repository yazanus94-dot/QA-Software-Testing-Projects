import pytest

from db_checks.api_client import BookerClient
from db_checks.booking_db import BookingDB


@pytest.fixture(scope="session")
def client():
    return BookerClient()


@pytest.fixture
def db():
    return BookingDB()  # fresh in-memory DB per test


@pytest.fixture
def payload():
    return {
        "firstname": "Yazan", "lastname": "DbCheck", "totalprice": 275, "depositpaid": True,
        "bookingdates": {"checkin": "2026-11-10", "checkout": "2026-11-12"}, "additionalneeds": "Parking",
    }


@pytest.fixture
def created(client, payload):
    """Creates a booking through the API and always cleans it up afterwards."""
    res = client.create(payload)
    yield res
    client.delete(res["bookingid"], client.token())
