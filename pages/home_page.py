from playwright.sync_api import expect

from config.settings import BASE_URL
from pages.base_page import BasePage


class HomePage(BasePage):
    def load(self) -> None:
        self.page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30000)

        print("\n[DEBUG] Home URL:", self.page.url)
        print("[DEBUG] Home title:", self.page.title())
        print("[DEBUG] First 1000 chars of body:")
        print(self.page.locator("body").inner_text()[:1000])

    def ensure_home_loaded(self) -> None:
        if "automationexercise.com" not in self.page.url:
            print("[FIX] Not on automationexercise, forcing home page")
            self.page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30000)

        # אם חזרנו לדף אבל title/body עדיין משובשים, תן עוד טעינה קצרה
        self.page.wait_for_timeout(1500)

        if "google_vignette" in self.page.url:
            print("[FIX] Clearing google_vignette on home page")
            self.page.evaluate("window.location.hash = ''")
            self.page.wait_for_timeout(1000)

        expect(self.page.locator("body")).to_contain_text("AutomationExercise", timeout=15000)

    def click_signup_login(self) -> None:
        signup_link = self.page.get_by_text("Signup / Login")
        expect(signup_link).to_be_visible(timeout=15000)
        signup_link.click(force=True)
        self.page.wait_for_load_state("domcontentloaded")

    def verify_logged_in_as(self, username: str) -> None:
        expect(self.page.get_by_text(f"Logged in as {username}")).to_be_visible(timeout=15000)

    def click_logout(self) -> None:
        logout_link = self.page.get_by_text("Logout")
        expect(logout_link).to_be_visible(timeout=15000)
        logout_link.click(force=True)
        self.page.wait_for_load_state("domcontentloaded")