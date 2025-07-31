"""Combining all Page objects into one, will make it an eye candy for the reader (and writer) of the test"""

from login_page import LoginPage
from profile_page import ProfilePage
from withdraw_page import WithdrawPage

from playwright.sync_api import Page


class Pages:
    def __init__(self, page: Page):
        self.page = page
        self.login_page = LoginPage(page)
        self.profile_page = ProfilePage(page)
        self.withdraw_page = WithdrawPage(page)