from flask import session


def test_login(client, auth):
    response = auth.login()
    assert response.status_code == 302

    with client:
        client.get("/")
        session["user_id"] == 1


def test_logout(client, auth):
    response = auth.login()
    assert response.status_code == 302

    response = auth.logout()
    assert response.status_code == 302

    with client:
        response = client.get("/")
        session.get("user_id") == None
