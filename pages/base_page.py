from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self, url: str) -> None:
        self.page.goto(url)

    def expect_text_visible(self, text: str) -> None:
        expect(self.page.get_by_text(text)).to_be_visible()