from playwright.sync_api import expect

from config.settings import BASE_URL
from pages.base_page import BasePage


class HomePage(BasePage):
    def load(self) -> None:
        self.page.goto(BASE_URL, wait_until="load")

        print("\n[DEBUG] Home URL:", self.page.url)
        print("[DEBUG] Home title:", self.page.title())
        print("[DEBUG] First 1000 chars of body:")
        print(self.page.locator("body").inner_text()[:1000])

        expect(self.page).to_have_url(f"{BASE_URL}/")

        signup_link = self.page.get_by_text("Signup / Login")
        expect(signup_link).to_be_visible(timeout=10000)

    def click_signup_login(self) -> None:
        signup_link = self.page.get_by_text("Signup / Login")
        expect(signup_link).to_be_visible(timeout=10000)
        signup_link.click()

    def verify_logged_in_as(self, username: str) -> None:
        expect(self.page.locator("body")).to_contain_text(f"Logged in as {username}")

    def click_logout(self) -> None:
        logout_link = self.page.get_by_text("Logout")
        expect(logout_link).to_be_visible(timeout=10000)
        logout_link.click()