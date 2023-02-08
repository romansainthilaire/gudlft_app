from server import clubs

club = clubs[0]

BASE_URL = "http://localhost:5000"


def test_login_with_unregistered_email(page):
    page.goto(BASE_URL)
    page.get_by_label("Email:").click()
    page.get_by_label("Email:").fill("email.doesnotexist@gmail.com")
    page.get_by_role("button", name="Enter").click()
    assert page.title() == "Registration | GUDLFT"
    assert page.query_selector("#email-not-found-message") is not None


def test_login_clubs_list_logout(page):
    page.goto(BASE_URL)

    # login
    page.get_by_label("Email:").click()
    page.get_by_label("Email:").fill(club["email"])
    page.get_by_role("button", name="Enter").click()
    assert page.title() == "Summary | GUDLFT"
    assert page.query_selector("h2").inner_text() == f"Welcome, {club['email']}"

    # see list of clubs with their points
    page.get_by_role("link", name="See all clubs").click()
    assert page.title() == "List of clubs | GUDLFT"
    assert page.query_selector("strong").inner_text() == f"{club['name']} - {club['points']} points"

    # go back to welcome page
    page.get_by_role("button", name="Back").click()
    assert page.title() == "Summary | GUDLFT"

    # logout
    page.get_by_role("link", name="Logout").click()
    assert page.title() == "Registration | GUDLFT"
