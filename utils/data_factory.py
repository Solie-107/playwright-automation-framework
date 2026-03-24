from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass
class UserData:
    name: str
    email: str
    password: str
    first_name: str
    last_name: str
    company: str
    address1: str
    address2: str
    country: str
    state: str
    city: str
    zipcode: str
    mobile_number: str


def build_user() -> UserData:
    ts = int(time.time())

    return UserData(
        name=f"solie_user_{ts}",
        email=f"solie_{ts}@mailinator.com",
        password="Test@12345",
        first_name="Salomon",
        last_name="Meniwabe",
        company="QA Company",
        address1="123 Main Street",
        address2="Suite 5",
        country="Canada",
        state="Ontario",
        city="Toronto",
        zipcode="10001",
        mobile_number="0501234567",
    )