from assassin.cli import init_db_command


def test_init_db(cli, monkeypatch):
    class Recorder:
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr("assassin.cli.init_db", fake_init_db)

    result = cli.invoke(args=["init-db"])
    assert "Initialized" in result.output
    assert Recorder.called


def test_create_user(app, cli):
    with app.app_context():
        result = cli.invoke(args=["create-user", "user@example.com", "Test User", "1A"])
        assert result.exit_code == 0
        assert "Created user" in result.output


def test_list_users(app, cli):
    with app.app_context():
        result = cli.invoke(args=["list-users"])
        assert result.exit_code == 0
        assert result.output.count("\n") == 5


def test_update_targets(app, cli):
    with app.app_context():
        result = cli.invoke(args=["update-targets"])
        assert result.exit_code == 0
        assert "Updated targets" in result.output
