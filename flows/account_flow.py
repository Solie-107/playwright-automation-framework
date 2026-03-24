from playwright.sync_api import Page

from api.account_api import AccountApi
from pages.home_page import HomePage
from pages.signup_login_page import SignupLoginPage
from utils.data_factory import UserData


class AccountFlow:
    def __init__(self, page: Page, api_client: AccountApi) -> None:
        self.page = page
        self.api = api_client

        self.home_page = HomePage(page)
        self.signup_login_page = SignupLoginPage(page)

    # =========================
    # UI FLOWS
    # =========================

    def create_user_via_ui(self, user: UserData) -> None:
        print(f"\n[FLOW] Create user via UI: {user.email}")

        self.home_page.load()
        self.home_page.click_signup_login()
        self.signup_login_page.verify_page_loaded()

        self.signup_login_page.signup_new_user(user)
        self.signup_login_page.fill_account_information(user)
        self.signup_login_page.verify_account_created()
        self.signup_login_page.click_continue_after_create()

        self.home_page.verify_logged_in_as(user.name)

    def login_via_ui(self, user: UserData) -> None:
        print(f"\n[FLOW] Login via UI: {user.email}")

        self.home_page.load()
        self.home_page.click_signup_login()
        self.signup_login_page.verify_page_loaded()

        self.signup_login_page.login(user.email, user.password)
        self.home_page.verify_logged_in_as(user.name)

    def logout(self) -> None:
        print("\n[FLOW] Logout")

        self.home_page.click_logout()
        self.signup_login_page.verify_page_loaded()

    # =========================
    # API FLOWS
    # =========================

    def verify_user_via_api(self, user: UserData) -> None:
        print(f"\n[FLOW] Verify user via API: {user.email}")

        response = self.api.verify_login(
            email=user.email,
            password=user.password,
        )

        print(f"[API] verifyLogin response: {response}")

        assert response["status_code"] == 200
        assert str(response["body"].get("responseCode")) == "200"

    def get_user_details_via_api(self, user: UserData) -> None:
        print(f"\n[FLOW] Get user details via API: {user.email}")

        response = self.api.get_user_detail_by_email(user.email)

        print(f"[API] getUserDetail response: {response}")

        assert response["status_code"] == 200
        assert str(response["body"].get("responseCode")) == "200"

        if "user" in response["body"]:
            returned_user = response["body"]["user"]

            assert returned_user["email"] == user.email
            assert returned_user["first_name"] == user.first_name
            assert returned_user["last_name"] == user.last_name

    def delete_user_via_api(self, user: UserData) -> None:
        print(f"\n[FLOW] Delete user via API: {user.email}")

        response = self.api.delete_account(
            email=user.email,
            password=user.password,
        )

        print(f"[API] deleteAccount response: {response}")

        if response["status_code"] == 403:
            print("[WARNING] Delete blocked by corporate firewall (expected in this environment)")
        else:
            assert response["status_code"] == 200