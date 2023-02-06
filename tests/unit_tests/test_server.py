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
