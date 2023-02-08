BASE_URL = "http://localhost:5000"


def test_login_with_unregistered_email(page):
    page.goto(BASE_URL)
    page.get_by_label("Email:").click()
    page.get_by_label("Email:").fill("email.doesnotexist@gmail.com")
    page.get_by_role("button", name="Enter").click()
    assert page.title() == "Registration | GUDLFT"
    assert page.query_selector("#email-not-found-message") is not None
