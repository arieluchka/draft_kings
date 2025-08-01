
Original code:

```js
const { Builder, By } = require('selenium-webdriver');
async function testLogin() {
    let driver = await new Builder().forBrowser('chrome').build();
    try {
        await driver.get('https://example.com/login');
        await driver.findElement(By.id('username')).sendKeys('user');
        await driver.findElement(By.id('password')).sendKeys('pass');
        await driver.findElement(By.id('login-button')).click();
        let welcomeMessage = await
            driver.findElement(By.id('welcome')).getText();
        if (welcomeMessage !== 'Welcome User') {
            throw new Error('Login failed');
        }
        console.log('Login successful!');
    } catch (error) {
        console.error('Test failed:', error);
    } finally {
        await driver.quit();
    }
}

testLogin();
```

Python + playwright equivalent:

```python
import pytest
from playwright.async_api import async_playwright

async def test_login():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto('https://example.com/login')
            await page.locator('[id="username"]').fill('user')
            await page.locator('[id="password"]').fill('pass')
            await page.locator('[id="login-button"]').click()

            welcome_message = await page.locator('[id="login-button"]').text_content()
            if welcome_message != 'Welcome User':
                raise Exception('Login failed')
            print('Login successful!')
        except Exception as error:
            print(f'Test failed: {error}')
        finally:
            await browser.close()

if __name__ == '__main__':
    import asyncio
    asyncio.run(test_login())
```

---

(Note: i will use the sync playwright api from now on, to reduce visual clutter, and as playwright has auto-waits built-in into its methods)

<br>

<br>

<br>

## Issues with the code

### 1) Hard coded locators
The test is accessing different elements on the web-page, but the code that is used to locate the elements is hard-coded inside the test function. If we will have another test that will somehow use the login page, we will need to write this code again.

This will very fast turn into inefficient and unmaintainable code (and unreadable, because of the extra clutter), as if the elements would change, we would need to manually go and edit all of its occurrences.

Suggestion: Specify pages and their locators in a centralized Page objects/classes, in a globally accessible folder (like `/common`? as different tests can use the ui)

Example:

`/common/ui_pages/login_page.py`
```python
from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self._page = page
        
        self.username_field = page.locator('[id="username"]')
        self.password_field = page.locator('[id="password"]')
        self.login_button = page.locator('[id="login-button"]')
```


`some_test_file.py`
```python
import pytest
from common.ui_pages.login_page import LoginPage
from playwright.sync_api import sync_playwright


def test_login():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            page.goto('https://example.com/login')
            login_page = LoginPage(page)

            login_page.username_field.fill("User")
            login_page.password_field.fill("Password")
            login_page.login_button.click()
            ....
```

Now, if something in the elements would change/new elements would be added, we would only need to rewrite `/common/ui_pages/login_page.py`, **and in most cases we wouldn't even need to modify any test.**

(we can also move the page path inside the class, and have some basic methods like "navigate_to_page" and more)

### 2) invocation of the selenium web driver inside the test
This also contributes to extra unnecessary clutter (every test need to have this line).

**But more than that,** it is impossible to do session scoped configuration.
for example, if we would want to run the tests through a different browser, we will have to go over all tests and change the "chrome" to something else (like firefox/webkit), which is just silly.


we can create a central fixture that all tests will use, to receive a new web driver:

```python
import pytest
import os
from playwright.sync_api import sync_playwright

browser_type = os.getenv("BROWSERT_TYPE", "chromium")

@pytest.fixture()
def get_page():
    pw = sync_playwright().start()
    browser = getattr(pw, browser_type)
    page = browser.launch().new_page()

    yield page

    pw.stop()


def test_login(get_page):
    page = get_page
    try:
        page.goto('https://example.com/login')
        ...

```

Not only the test is much more clean and readable, we can also change configuration of the whole run/all the tests with ease.

### 3) Verify the user is logged in
This depends if the user is redirected to another page after login, or is he kept in the same page, but just a "welcome" pop-up appears.

<br>

**In case of rediracting to another page:**

If selenium wont be able to find the `#welcome` element, we wont even get to the `if (welcomeMessage !== 'Welcome User')` part.
Meaning, we will receive an error for not finding the element, before we check the element itself.


**also**, if the intention was to display a welcome message with the username (like: `Welcome Ariel`), then this test will need to be re-written if we will want to run with another user.

### 4) user+password are hardcoded
Makes it very hard to re-use this test with other credentials

### 5) Loggin in and  Validation that the user is logged in could be a general function/method
As we would probably want to validate that on every login for every other test. 

(ideally can be inside the Page Object, as it's directly connected to the LoginPage, and will be used in other tests)

### 6) The initial URL is hardcoded
Impossible to adapt tests to other TLDs or urls (when in different environments, for example)

### 7) Function name is uninformative