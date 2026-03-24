from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.signup_login_page import SignupLoginPage
from utils.data_factory import UserData


def test_user_can_signup_and_login(page: Page, user_data: UserData) -> None:
    home_page = HomePage(page)
    signup_login_page = SignupLoginPage(page)

    # Open site
    home_page.load()

    # Go to Signup/Login
    home_page.click_signup_login()
    signup_login_page.verify_page_loaded()

    # Signup
    signup_login_page.signup_new_user(user_data)
    signup_login_page.fill_account_information(user_data)
    signup_login_page.verify_account_created()
    signup_login_page.click_continue_after_create()

    # Verify logged in
    home_page.verify_logged_in_as(user_data.name)

    # Logout
    home_page.click_logout()
    signup_login_page.verify_page_loaded()

    # Login again
    signup_login_page.login(user_data.email, user_data.password)
    home_page.verify_logged_in_as(user_data.name)


def test_signup_with_invalid_email_shows_browser_validation(page: Page) -> None:
    home_page = HomePage(page)
    signup_login_page = SignupLoginPage(page)

    home_page.load()
    home_page.click_signup_login()
    signup_login_page.verify_page_loaded()

    page.locator("[data-qa='signup-name']").fill("Salomon")
    page.locator("[data-qa='signup-email']").fill("invalid-email")
    page.locator("[data-qa='signup-button']").click()

    validation_message = page.locator("[data-qa='signup-email']").evaluate(
        "el => el.validationMessage"
    )

    assert validation_message != ""


def test_signup_with_empty_email_shows_browser_validation(page: Page) -> None:
    home_page = HomePage(page)
    signup_login_page = SignupLoginPage(page)

    home_page.load()
    home_page.click_signup_login()
    signup_login_page.verify_page_loaded()

    page.locator("[data-qa='signup-name']").fill("Salomon")
    page.locator("[data-qa='signup-email']").fill("")
    page.locator("[data-qa='signup-button']").click()

    validation_message = page.locator("[data-qa='signup-email']").evaluate(
        "el => el.validationMessage"
    )

    assert validation_message != ""


def test_login_with_wrong_password_shows_error(
    page: Page,
    user_data: UserData,
) -> None:
    home_page = HomePage(page)
    signup_login_page = SignupLoginPage(page)

    # Create user first
    home_page.load()
    home_page.click_signup_login()
    signup_login_page.verify_page_loaded()

    signup_login_page.signup_new_user(user_data)
    signup_login_page.fill_account_information(user_data)
    signup_login_page.verify_account_created()
    signup_login_page.click_continue_after_create()
    home_page.verify_logged_in_as(user_data.name)

    # Logout
    home_page.click_logout()
    signup_login_page.verify_page_loaded()

    # Try wrong login
    signup_login_page.login(user_data.email, "WrongPassword123")

    expect(page.locator("body")).to_contain_text("Your email or password is incorrect!")