from __future__ import annotations
import json
from typing import Any
from playwright.sync_api import APIRequestContext
from config.settings import API_BASE_URL
from utils.data_factory import UserData


class AccountApi:
    def __init__(self, request_context: APIRequestContext) -> None:
        self.request_context = request_context

    @staticmethod
    def _safe_json(response_text: str) -> dict[str, Any]:
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            return {"raw_text": response_text}

    def verify_login(self, email: str, password: str) -> dict[str, Any]:
        response = self.request_context.post(
            f"{API_BASE_URL}/verifyLogin",
            form={
                "email": email,
                "password": password,
            },
        )
        return {
            "status_code": response.status,
            "body": self._safe_json(response.text()),
        }

    def get_user_detail_by_email(self, email: str) -> dict[str, Any]:
        response = self.request_context.get(
            f"{API_BASE_URL}/getUserDetailByEmail",
            params={"email": email},
        )
        return {
            "status_code": response.status,
            "body": self._safe_json(response.text()),
        }

    def delete_account(self, email: str, password: str) -> dict[str, Any]:
        response = self.request_context.delete(
            f"{API_BASE_URL}/deleteAccount",
            form={
                "email": email,
                "password": password,
            },
        )
        return {
            "status_code": response.status,
            "body": self._safe_json(response.text()),
        }

    def create_account(self, user: UserData) -> dict[str, Any]:
        response = self.request_context.post(
            f"{API_BASE_URL}/createAccount",
            form={
                "name": user.name,
                "email": user.email,
                "password": user.password,
                "title": "Mr",
                "birth_date": "1",
                "birth_month": "1",
                "birth_year": "2000",
                "firstname": user.first_name,
                "lastname": user.last_name,
                "company": user.company,
                "address1": user.address1,
                "address2": user.address2,
                "country": user.country,
                "zipcode": user.zipcode,
                "state": user.state,
                "city": user.city,
                "mobile_number": user.mobile_number,
            },
        )
        return {
            "status_code": response.status,
            "body": self._safe_json(response.text()),
        }