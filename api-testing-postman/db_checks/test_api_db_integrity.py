"""API ↔ Database consistency checks (pytest).

Flow: call the API -> persist the response in the DB -> verify the stored row equals the
API's view of the same record (and that DB constraints reject invalid business data).
"""
import sqlite3

import pytest

pytestmark = pytest.mark.db


def test_created_booking_is_persisted_correctly(client, db, created, payload):
    booking_id = created["bookingid"]
    db.save(booking_id, created["booking"])

    row = db.get(booking_id)
    assert row is not None
    assert (row["firstname"], row["lastname"]) == (payload["firstname"], payload["lastname"])
    assert row["totalprice"] == payload["totalprice"]
    assert bool(row["depositpaid"]) is payload["depositpaid"]
    assert row["checkin"] == payload["bookingdates"]["checkin"]


def test_db_row_matches_fresh_api_read(client, db, created):
    booking_id = created["bookingid"]
    db.save(booking_id, created["booking"])

    api = client.get(booking_id).json()
    row = db.get(booking_id)
    assert row["firstname"] == api["firstname"]
    assert row["totalprice"] == api["totalprice"]
    assert row["checkout"] == api["bookingdates"]["checkout"]


def test_deleted_booking_is_absent_from_api_and_db(client, db, created):
    booking_id = created["bookingid"]
    db.save(booking_id, created["booking"])

    assert client.delete(booking_id, client.token()).status_code == 201
    db.delete(booking_id)

    assert client.get(booking_id).status_code == 404
    assert db.get(booking_id) is None


def test_booking_ids_are_unique(client, payload):
    ids = []
    try:
        for _ in range(3):
            ids.append(client.create(payload)["bookingid"])
        assert len(ids) == len(set(ids))
    finally:
        token = client.token()
        for i in ids:
            client.delete(i, token)


def test_db_constraints_reject_invalid_business_data(db, payload):
    bad = {**payload, "bookingdates": {"checkin": "2026-11-12", "checkout": "2026-11-10"}}
    with pytest.raises(sqlite3.IntegrityError):
        db.save(1, bad)  # checkout before checkin must never be stored

    negative_price = {**payload, "totalprice": -5}
    with pytest.raises(sqlite3.IntegrityError):
        db.save(2, negative_price)
