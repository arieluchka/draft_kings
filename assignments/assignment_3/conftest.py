"""this will make fixtures accessible to all child tests"""
import pytest
import os
from common.ui_pages.pages import Pages
from playwright.sync_api import sync_playwright, Page

BASE_URL = os.getenv("BASE_URL", "https://example.com")
BROWSER_TYPE = os.getenv("BROWSERT_TYPE", "chromium")

@pytest.fixture()
def test_user():
    TEST_USERNAME = os.getenv("TEST_USERNAME", "user")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD", "pass")
    return TEST_USERNAME, TEST_PASSWORD


@pytest.fixture()
def get_page() -> Page:
    pw = sync_playwright().start()
    browser = getattr(pw, BROWSER_TYPE)
    page: Page = browser.launch().new_page()

    yield page

    pw.stop()

@pytest.fixture()
def pages(request, get_page) -> Pages:
    first_path = request.param
    get_page.goto(BASE_URL + first_path)

    return Pages(get_page)