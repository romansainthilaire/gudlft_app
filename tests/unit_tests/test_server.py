from datetime import datetime

from server import clubs, competitions


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_login_with_registered_email(client):
    club = clubs[0]
    data = {"email": club["email"]}
    response = client.post("/show_summary", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert bytes(club["points"], "utf8") in response.data
    for competition in competitions:
        assert bytes(competition["name"], "utf8") in response.data


def test_login_with_unregistered_email(client):
    data = {"email": "test@gmail.com"}
    response = client.post("/show_summary", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"email-not-found-message" in response.data


def test_logout(client):
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b'type="email"' in response.data


def test_get_booking_page_with_registered_future_competition_and_registered_club(client):
    club = clubs[0]
    future_competition = [
        c for c in competitions if datetime.strptime(c["date"], '%Y-%m-%d %H:%M:%S') > datetime.now()
        ][0]
    response = client.get(f"/book/{future_competition['name']}/{club['name']}", follow_redirects=True)
    assert response.status_code == 200
    assert bytes(future_competition["name"], "utf8") in response.data
    assert bytes(future_competition["numberOfPlaces"], "utf8") in response.data


def test_get_booking_page_with_unregistered_competition(client):
    club = clubs[0]
    competition = {"name": "Competition does not exist", "date": "9999-01-01 00:00:00", "numberOfPlaces": "10"}
    response = client.get(f"/book/{competition['name']}/{club['name']}", follow_redirects=True)
    assert response.status_code == 404
