from server import clubs, future_competitions

club = clubs[0]
competition = future_competitions[0]

BASE_URL = "http://localhost:5000"


def test_login_with_unregistered_email(page):
    page.goto(BASE_URL)
    page.get_by_label("Email:").click()
    page.get_by_label("Email:").fill("email.doesnotexist@gmail.com")
    page.get_by_role("button", name="Enter").click()
    assert page.title() == "Registration | GUDLFT"
    assert page.query_selector("li").inner_text() == "Sorry, that email wasn't found."


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


def test_login_book_15_places(page):
    page.goto(BASE_URL)
    purchased_places = 15

    # login
    page.get_by_label("Email:").click()
    page.get_by_label("Email:").fill(club["email"])
    page.get_by_role("button", name="Enter").click()

    # book places
    (page
     .get_by_role("paragraph")
     .filter(has_text=(
         f"{competition['name']} " +
         f"Date: {competition['date']} " +
         f"Places left: {competition['numberOfPlaces']} " +
         "Book Places"))
     .get_by_role("link", name="Book Places")
     .click())
    page.get_by_label("How many places?").click()
    page.get_by_label("How many places?").fill(str(purchased_places))
    page.get_by_role("button", name="Book").click()
    assert page.title() == f"Booking for {competition['name']} | GUDLFT"
    assert page.query_selector("li").inner_text() == "You can book 12 places max per competition."


def test_login_book_10_places(page):
    page.goto(BASE_URL)
    purchased_places = 10

    # login
    page.get_by_label("Email:").click()
    page.get_by_label("Email:").fill(club["email"])
    page.get_by_role("button", name="Enter").click()

    # book places
    (page
     .get_by_role("paragraph")
     .filter(has_text=(
         f"{competition['name']} " +
         f"Date: {competition['date']} " +
         f"Places left: {competition['numberOfPlaces']} " +
         "Book Places"))
     .get_by_role("link", name="Book Places")
     .click())
    page.get_by_label("How many places?").click()
    page.get_by_label("How many places?").fill(str(purchased_places))
    page.get_by_role("button", name="Book").click()
    assert page.title() == "Summary | GUDLFT"
    assert (page
            .query_selector("#points-available")
            .inner_text() == f"Points available: {club['points'] - purchased_places}")
