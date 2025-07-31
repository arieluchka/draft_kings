import pytest

@pytest.mark.parametrize("pages", ["/login"], indirect=True)
def test_login_with_correct_credentials(pages, test_user):
    username, password = test_user
    pages.login_page.log_in(
        username=username,
        password=password
    )
    pages.login_page.verify_user_is_logged_in(
        username=username # assuming the message is per User
    )

    # THE "get_page" FIXTURE WILL CLOSE PLAYWRIGHT, WHETHER TEST PASSED OR FAILED


###### OR



@pytest.mark.parametrize("pages", ["/login"], indirect=True)
@pytest.mark.parametrize("user_creds", [
    ("user1", "password1"),
    ("Ariel", "qwerty123"),
    ("Yoram", "YoramHaGever420")
])
def test_login_with_different_credentials(pages, user_creds):
    username, password = user_creds
    pages.login_page.log_in(
        username=username,
        password=password
    )
    pages.login_page.verify_user_is_logged_in(
        username=username # assuming the message is per User
    )