"""Central configuration. Everything can be overridden with environment variables."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

APPIUM_URL = os.getenv("APPIUM_URL", "http://127.0.0.1:4723")
APP_PATH = os.getenv("APP_PATH", str(ROOT / "apps" / "mda-app.apk"))
DEVICE_NAME = os.getenv("DEVICE_NAME", "Android Emulator")
PLATFORM_VERSION = os.getenv("PLATFORM_VERSION", "")  # empty = whatever is connected
APP_PACKAGE = os.getenv("APP_PACKAGE", "com.saucelabs.mydemoapp.android")
IMPLICIT_WAIT = 0  # we use explicit waits only (best practice)
EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "15"))

VALID_USER = {"email": "bob@example.com", "password": "10203040"}
LOCKED_USER = {"email": "alice@example.com", "password": "10203040"}
