from assassin.db import get_db, queries


def get_targets(db):
    return db.execute("select hunter_id, prey_id from target").fetchall()


def get_assassinations(db):
    return db.execute("select hunter_id, prey_id from assassination").fetchall()


def test_get_user(app):
    with app.app_context():
        db = get_db()

        user = queries.get_user(db, id=None)
        assert user == None

        user = queries.get_user(db, id=1)
        assert user["name"] == "User 1"


def test_get_user_by_email(app):
    with app.app_context():
        db = get_db()

        user = queries.get_user_by_email(db, email=None)
        assert user == None

        user = queries.get_user_by_email(db, email="user1@example.com")
        assert user["name"] == "User 1"


def test_create_user(app):
    user_info = {"email": "user@example.com", "name": "Test User", "location": "1A"}

    with app.app_context():
        db = get_db()

        user_id = queries.create_user(db, **user_info)
        assert user_id != None
        db.commit()

        user = queries.get_user(db, user_id)
        for k, v in user_info.items():
            assert user[k] == v

        assert user["is_active"] == True


def test_target_view(app):
    with app.app_context():
        db = get_db()
        targets = list(map(dict, get_targets(db)))
        assert len(targets) == 3
        assert {"hunter_id": 1, "prey_id": 2} in targets
        assert {"hunter_id": 2, "prey_id": 3} in targets
        assert {"hunter_id": 3, "prey_id": 1} in targets


def test_update_targets(app):
    with app.app_context():
        db = get_db()
        queries.update_targets(db)
        db.commit()

        targets = get_targets(db)
        assert len(targets) == 3


def test_create_assassination(app):
    with app.app_context():
        db = get_db()
        assassinations = get_assassinations(db)
        assert len(assassinations) == 3

        queries.create_assassination(db, prey_id=2)
        db.commit()
        assassinations = get_assassinations(db)
        assert len(assassinations) == 4

        targets = list(map(dict, get_targets(db)))
        assert len(targets) == 2
        assert {"hunter_id": 1, "prey_id": 3} in targets
        assert {"hunter_id": 3, "prey_id": 1} in targets


def test_get_home_data(app):
    expected = {
        "is_active": True,
        "has_hunter": True,
        "prey_name": "User 2",
        "prey_location": "2A",
    }

    with app.app_context():
        db = get_db()
        home_data = queries.get_home_data(db, id=1)
        assert dict(home_data) == expected


def test_get_leaderboard_data(app):
    expected = [
        {"name": "User 1", "location": "1A", "score": 2},
        {"name": "User 3", "location": "3A", "score": 1},
        {"name": "User 2", "location": "2A", "score": 0},
        {"name": "User 4", "location": "4A", "score": 0},
        {"name": "User 5", "location": "5A", "score": 0},
    ]

    with app.app_context():
        db = get_db()
        home_data = list(map(dict, queries.get_leaderboard_data(db)))
        assert home_data == expected
