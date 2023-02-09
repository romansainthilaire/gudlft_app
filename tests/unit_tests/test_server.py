from server import clubs, competitions, past_competitions, future_competitions

club = clubs[0]
past_competition = past_competitions[0]
future_competition = future_competitions[0]


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_login_with_registered_email(client):
    data = {"email": club["email"]}
    response = client.post("/show_summary", data=data, follow_redirects=True)
    assert response.status_code == 200
    for competition in competitions:
        assert bytes(competition["name"], "utf8") in response.data


def test_login_with_unregistered_email(client):
    data = {"email": "email.doesnotexist@gmail.com"}
    response = client.post("/show_summary", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"email-not-found-message" in response.data


def test_logout(client):
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b'type="email"' in response.data


def test_page_not_found(client):
    response = client.get("/endpoint-does-not-exist")
    assert response.status_code == 404


def test_get_booking_page_with_registered_future_competition(client):
    response = client.get(f"/book/{future_competition['name']}/{club['name']}", follow_redirects=True)
    assert response.status_code == 200
    assert bytes(future_competition["name"], "utf8") in response.data
    assert bytes(str(future_competition["numberOfPlaces"]), "utf8") in response.data


def test_get_booking_page_with_registered_past_competition(client):
    response = client.get(f"/book/{past_competition['name']}/{club['name']}", follow_redirects=True)
    assert response.status_code == 403


def test_update_club_points_after_purchasing_places(client):
    club["points"] = 10
    future_competition["numberOfPlaces"] = 20
    places_purchased = 5
    data = {"club": club["name"], "competition": future_competition["name"], "places": places_purchased}
    response = client.post("/purchase_places", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert club["points"] == 5
    assert b"booking-complete-message" in response.data


def test_purchase_places_without_enough_points(client):
    club["points"] = 5
    future_competition["numberOfPlaces"] = 20
    places_purchased = 10
    data = {"club": club["name"], "competition": future_competition["name"], "places": places_purchased}
    response = client.post("/purchase_places", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"not-enough-points-message" in response.data


def test_purchase_more_places_than_places_left(client):
    club["points"] = 20
    future_competition["numberOfPlaces"] = 5
    places_purchased = 10
    data = {"club": club["name"], "competition": future_competition["name"], "places": places_purchased}
    response = client.post("/purchase_places", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"not-enough-places-left-message" in response.data


def test_purchase_more_than_12_places(client):
    club["points"] = 20
    future_competition["numberOfPlaces"] = 30
    places_purchased = 15
    data = {"club": club["name"], "competition": future_competition["name"], "places": places_purchased}
    response = client.post("/purchase_places", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"12-places-max-message" in response.data


def test_purchase_negative_number_of_places(client):
    club["points"] = 10
    future_competition["numberOfPlaces"] = 20
    places_purchased = -5
    data = {"club": club["name"], "competition": future_competition["name"], "places": places_purchased}
    response = client.post("/purchase_places", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"invalid-number-of-places-message" in response.data


def test_purchase_empty_value(client):
    club["points"] = 10
    future_competition["numberOfPlaces"] = 20
    places_purchased = ""
    data = {"club": club["name"], "competition": future_competition["name"], "places": places_purchased}
    response = client.post("/purchase_places", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"invalid-number-of-places-message" in response.data


def test_points_display_board(client):
    response = client.get(f"/clubs/{club['name']}", follow_redirects=True)
    assert response.status_code == 200
    for c in clubs:
        assert bytes(c["name"], "utf8") in response.data
        assert bytes(str(c["points"]), "utf8") in response.data
