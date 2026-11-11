"""Tiny SQLite 'system of record' that mirrors what the API returns.

In a real project this would be the application's own database; here it lets us demonstrate
how to verify API responses against persisted data (and detect drift) without any infrastructure.
"""
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS bookings (
    booking_id      INTEGER PRIMARY KEY,
    firstname       TEXT NOT NULL,
    lastname        TEXT NOT NULL,
    totalprice      INTEGER NOT NULL CHECK (totalprice >= 0),
    depositpaid     INTEGER NOT NULL CHECK (depositpaid IN (0,1)),
    checkin         TEXT NOT NULL,
    checkout        TEXT NOT NULL,
    additionalneeds TEXT,
    CHECK (checkout >= checkin)
);
"""


class BookingDB:
    def __init__(self, path: str = ":memory:"):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def save(self, booking_id: int, b: dict) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO bookings VALUES (?,?,?,?,?,?,?,?)",
            (booking_id, b["firstname"], b["lastname"], b["totalprice"], int(b["depositpaid"]),
             b["bookingdates"]["checkin"], b["bookingdates"]["checkout"], b.get("additionalneeds")),
        )
        self.conn.commit()

    def get(self, booking_id: int):
        return self.conn.execute("SELECT * FROM bookings WHERE booking_id=?", (booking_id,)).fetchone()

    def count(self) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]

    def delete(self, booking_id: int) -> None:
        self.conn.execute("DELETE FROM bookings WHERE booking_id=?", (booking_id,))
        self.conn.commit()
