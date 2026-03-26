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

        self.page.wait_for_selector("[data-qa='password']", timeout=15000)
        print("[DEBUG] Page ready")

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

        create_button = self.page.locator("[data-qa='create-account']")
        create_button.scroll_into_view_if_needed()
        expect(create_button).to_be_visible(timeout=10000)
        expect(create_button).to_be_enabled(timeout=10000)
        create_button.click(force=True)

        if "google_vignette" in self.page.url:
            print("[WARNING] google_vignette detected after submit, clearing hash")
            self.page.evaluate("window.location.hash = ''")
            self.page.wait_for_timeout(1000)


    def verify_account_created(self) -> None:
        print(f"[DEBUG] Current URL: {self.page.url}")

        if "google_vignette" in self.page.url:
            print("[WARNING] google_vignette detected, clearing hash")
            self.page.evaluate("window.location.hash = ''")
            self.page.wait_for_timeout(1000)
        elif "automationexercise.com" not in self.page.url:
            print("[WARNING] External redirect detected, going back")
            self.page.go_back()
            self.page.wait_for_load_state("load")

        expect(self.page.locator("body")).to_contain_text("Account Created!", timeout=15000)
        expect(self.page.locator("[data-qa='continue-button']")).to_be_visible(timeout=15000)


    def click_continue_after_create(self) -> None:
        print(f"[DEBUG] Before continue URL: {self.page.url}")

        # ניקוי vignette
        if "google_vignette" in self.page.url:
            print("[FIX] Removing google_vignette")
            self.page.evaluate("window.location.hash = ''")
            self.page.wait_for_timeout(1000)

        # ניסיון רגיל
        continue_button = self.page.locator("[data-qa='continue-button']")

        if continue_button.is_visible():
            print("[DEBUG] Clicking continue button")
            continue_button.click(force=True)
            self.page.wait_for_load_state("load")

        # ❗ fallback חזק (זה הקסם)
        if "account_created" in self.page.url:
            print("[FIX] Still on account_created → forcing navigation to home")
            self.page.goto("https://automationexercise.com/")
            self.page.wait_for_load_state("load")

        print(f"[DEBUG] After continue URL: {self.page.url}")


    def login(self, email: str, password: str) -> None:
        print(f"[DEBUG] Performing login for: {email}")

        email_input = self.page.locator("[data-qa='login-email']")
        password_input = self.page.locator("[data-qa='login-password']")
        login_button = self.page.locator("[data-qa='login-button']")

        email_input.fill(email)
        password_input.fill(password)

        login_button.scroll_into_view_if_needed()
        login_button.click(force=True)

        self.page.wait_for_load_state("load")