from assassin.db import get_db, queries


def test_home_not_logged_in(client):
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert b"You must login" in response.data


def test_home_logged_in(auth, client):
    # active has target
    auth.login(email="user1@example.com")
    response = client.get("/")
    assert response.status_code == 200
    assert b"User 2" in response.data
    assert b"2A" in response.data
    assert b"I've been assassinated" in response.data

    # inactive has target
    auth.login(email="user2@example.com")
    response = client.get("/")
    assert response.status_code == 200
    assert b"User 3" in response.data
    assert b"3A" in response.data
    assert b"Your participation is paused" in response.data
    assert b"I've been assassinated" in response.data

    # active no target
    auth.login(email="user4@example.com")
    response = client.get("/")
    assert response.status_code == 200
    assert b"You don't have a target right now" in response.data
    assert b"I've been assassinated" not in response.data

    # inactive no target
    auth.login(email="user5@example.com")
    response = client.get("/")
    assert response.status_code == 200
    assert b"You don't have a target right now" in response.data
    assert b"Your participation is paused" in response.data
    assert b"I've been assassinated" not in response.data


def test_home_record_assassination(auth, client):
    auth.login()
    response = client.post(
        "/", data={"kind": "record_assassination"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Assassination recorded" in response.data
    assert b"You don't have a target right now" in response.data


def test_home_set_is_active(auth, client):
    auth.login()

    # set inactive
    response = client.post(
        "/", data={"kind": "set_is_active", "is_active": "false"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Participation paused" in response.data
    assert b"Your participation is paused" in response.data

    # set active
    response = client.post(
        "/", data={"kind": "set_is_active", "is_active": "true"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Participation resumed" in response.data
    assert b"Your participation is paused" not in response.data


def test_leaderboard(app, client):
    response = client.get("/leaderboard")
    assert response.status_code == 200

    with app.app_context():
        for row in queries.get_leaderboard_data(get_db()):
            for val in row:
                assert bytes(str(val), "utf-8") in response.data
