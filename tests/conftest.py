import os
import tempfile

import pytest

from assassin import create_app
from assassin.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({"TESTING": True, "SECRET_KEY": "test", "DATABASE": db_path})

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def cli(app):
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client, monkeypatch):
        self._client = client
        self._monkeypatch = monkeypatch

    def login(self, email="user1@example.com", error=False):
        def fake_acquire_token_by_auth_code_flow():
            if error:
                return {"error": {}}
            else:
                return {"id_token_claims": {"preferred_username": email}}

        self._monkeypatch.setattr(
            "assassin.auth.acquire_token_by_auth_code_flow",
            fake_acquire_token_by_auth_code_flow,
        )

        return self._client.get("/auth/redirect")

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client, monkeypatch):
    return AuthActions(client, monkeypatch)
