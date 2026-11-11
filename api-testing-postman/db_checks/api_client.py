"""Thin Restful-Booker client used by the DB-integrity tests."""
import os

import requests

BASE_URL = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")


class BookerClient:
    def __init__(self, base_url: str = BASE_URL, timeout: int = 15):
        self.base = base_url.rstrip("/")
        self.timeout = timeout
        self.s = requests.Session()
        self.s.headers.update({"Content-Type": "application/json", "Accept": "application/json"})

    def token(self) -> str:
        r = self.s.post(f"{self.base}/auth", json={"username": "admin", "password": "password123"}, timeout=self.timeout)
        r.raise_for_status()
        return r.json()["token"]

    def create(self, payload: dict) -> dict:
        r = self.s.post(f"{self.base}/booking", json=payload, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def get(self, booking_id: int) -> requests.Response:
        return self.s.get(f"{self.base}/booking/{booking_id}", timeout=self.timeout)

    def delete(self, booking_id: int, token: str) -> requests.Response:
        return self.s.delete(f"{self.base}/booking/{booking_id}", headers={"Cookie": f"token={token}"}, timeout=self.timeout)
