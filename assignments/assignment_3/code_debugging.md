
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

## Issues with the code

### 1) Hard coded locators
The test is accessing different elements on the web-page, but the code that is used to locate the elements is hard-coded inside the test function. If we will have another test that will somehow use the login page, we will need to write this code again.

This will very fast turn into inefficient and unmaintainable code (and unreadable, because of the extra clutter), as if the elements would change, we would need to manually go and edit all of its occurrences.

Suggestion: Specify pages and their locators in a centralized Page object.

Example:

