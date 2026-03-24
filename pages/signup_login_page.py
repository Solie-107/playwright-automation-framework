from playwright.sync_api import expect

from pages.base_page import BasePage
from utils.data_factory import UserData


class SignupLoginPage(BasePage):
    def verify_page_loaded(self) -> None:
        expect(self.page.get_by_text("Login to your account")).to_be_visible()
        expect(self.page.get_by_text("New User Signup!")).to_be_visible()

    def signup_new_user(self, user: UserData) -> None:
        self.page.locator("[data-qa='signup-name']").fill(user.name)
        self.page.locator("[data-qa='signup-email']").fill(user.email)
        self.page.locator("[data-qa='signup-button']").click()

    def fill_account_information(self, user: UserData) -> None:
        print("\n[FLOW] Waiting for Account Information page...")

    # חכה לאלמנט אמיתי
        self.page.wait_for_selector("[data-qa='password']", timeout=15000)

        print("[DEBUG] Page ready")

    # ❗ אל תיגע ב-gender בכלל
    # זה לא חובה באתר הזה

        self.page.locator("[data-qa='password']").fill(user.password)

        self.page.locator("[data-qa='days']").select_option("1")
        self.page.locator("[data-qa='months']").select_option("1")
        self.page.locator("[data-qa='years']").select_option("2000")

        self.page.locator("[data-qa='first_name']").fill(user.first_name)
        self.page.locator("[data-qa='last_name']").fill(user.last_name)
        self.page.locator("[data-qa='company']").fill(user.company)
        self.page.locator("[data-qa='address']").fill(user.address1)
        self.page.locator("[data-qa='address2']").fill(user.address2)
        self.page.locator("[data-qa='country']").select_option(user.country)
        self.page.locator("[data-qa='state']").fill(user.state)
        self.page.locator("[data-qa='city']").fill(user.city)
        self.page.locator("[data-qa='zipcode']").fill(user.zipcode)
        self.page.locator("[data-qa='mobile_number']").fill(user.mobile_number)

        self.page.locator("[data-qa='create-account']").click()
    def verify_account_created(self) -> None:
        expect(self.page.locator("body")).to_contain_text("Account Created!")

    def click_continue_after_create(self) -> None:
        self.page.locator("[data-qa='continue-button']").click()

    def login(self, email: str, password: str) -> None:
        self.page.locator("[data-qa='login-email']").fill(email)
        self.page.locator("[data-qa='login-password']").fill(password)
        self.page.locator("[data-qa='login-button']").click()