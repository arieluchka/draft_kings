## 3) Code Debugging

3 issues/bad practices

1) the browser is invoked inside the test.

every test will need this repetative line + makes it non easily configurable for other browsers (firefox/webkit)

2) login path inside test (repetative, harder to maintain if the domain/TLD changes)

3) directly accessing ids and web elements/locators throught the tests. 
If a certain locator changes, we will need to go through all the tests that have it, and modify it.

Solution: Use POM (Page Object Models)

4) User+Password are hardcoded inside test. a) if they change, harder to maintain. b) we cant parameterize/reuse the test in the future, for different users.

5) Throwing general error instead of specific error type?

6) the catch will catch all errors, whether it is the error the test raised or a different one.

7) ids in the UI are not descriptive enough

8) if login message slightly changes (for example if the username in the message is per signing user), it will fail (unless we modify the hardcoded message).

Solution: either replace "User" with variable of the user that was logged in (unless it's literally says "Welcome User" for all users), or search for a REGEX message, that starts with "^Welcome .*" 
