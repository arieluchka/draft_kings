
from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self._page = page

        self.username_field = page.locator('[id="username"]')
        self.password_field = page.locator('[id="password"]')
        self.login_button = page.locator('[id="login-button"]')

        self.welcome_message = page.locator('[id="welcome"]')

    def verify_user_is_logged_in(self, username):
        assert self.welcome_message.inner_text() == f"Welcome {username}"
        return True

    def log_in(self, username, password):
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.login_button.click()

