from server import clubs, future_competitions

club = clubs[0]
competition = future_competitions[0]

BASE_URL = "http://localhost:5000"


def login(page, email):
    page.goto(BASE_URL)
    page.get_by_label("Email:").fill(email)
    page.get_by_role("button", name="Enter").click()


def test_login_with_unregistered_email(page):

    # try to login and get error message
    login(page, "email.doesnotexist@gmail.com")
    assert page.title() == "Registration | GUDLFT"
    assert page.query_selector("li").inner_text() == "Sorry, that email wasn't found."


def test_login_clubs_list_logout(page):

    # login
    login(page, club["email"])
    assert page.title() == "Summary | GUDLFT"
    assert page.query_selector("h2").inner_text() == f"Welcome, {club['email']}"

    # go see list of clubs with their points
    page.get_by_role("link", name="See all clubs").click()
    assert page.title() == "List of clubs | GUDLFT"
    assert page.query_selector("strong").inner_text() == f"{club['name']} - {club['points']} points"

    # go back to welcome page
    page.get_by_role("button", name="Back").click()
    assert page.title() == "Summary | GUDLFT"

    # logout
    page.get_by_role("link", name="Logout").click()
    assert page.title() == "Registration | GUDLFT"


def purchase_n_places(page, n):
    (page
     .get_by_role("paragraph")
     .filter(has_text=(
         f"{competition['name']} " +
         f"Date: {competition['date']} " +
         f"Places left: {competition['numberOfPlaces']} " +
         "Book Places"))
     .get_by_role("link", name="Book Places")
     .click())
    page.get_by_label("How many places?").fill(str(n))
    page.get_by_role("button", name="Book").click()


def test_login_purchase_15_places(page):

    # login
    login(page, club["email"])

    # try to book 15 places et get error message (12 places max)
    purchase_n_places(page, 15)
    assert page.title() == f"Booking for {competition['name']} | GUDLFT"
    assert page.query_selector("li").inner_text() == "You can book 12 places max per competition."


def test_login_purchase_10_places(page):

    # login
    login(page, club["email"])

    # book 10 places and get redirected to summary
    purchase_n_places(page, 10)
    assert page.title() == "Summary | GUDLFT"
    assert page.query_selector("li").inner_text() == "Great-booking complete!"
    assert (page
            .query_selector("#points-available")
            .inner_text() == f"Points available: {club['points'] - 10}")
