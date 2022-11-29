import sqlite3
from datetime import datetime

import click
from flask import current_app

from .db import get_db, init_db, queries


@click.command("init-db")
def init_db_command():
    """Create database"""
    init_db()
    click.echo("Initialized database.")


@click.command("backup-db")
def backup_db():
    """Backup the database"""
    db = get_db()
    timestamp = datetime.now().isoformat()
    backup_db = sqlite3.connect(current_app.config["DATABASE"] + "." + timestamp)

    with backup_db:
        db.backup(backup_db, pages=1)


@click.command("create-user")
@click.argument("email")
@click.argument("name")
@click.argument("wing")
def create_user(email, name, wing):
    """Create a new user."""
    db = get_db()
    user_id = queries.create_user(db, email, name, wing)
    db.commit()
    click.echo(f"Created user with id={user_id}.")


@click.command("list-users")
def get_all_users():
    """List users in database."""
    for user in queries.get_all_users(get_db()):
        click.echo(dict(user))


@click.command("update-targets")
def update_targets():
    """Assigns new targets to all active users."""
    queries.update_targets(get_db())
    click.echo("Updated targets.")


def init_app(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(backup_db)
    app.cli.add_command(create_user)
    app.cli.add_command(get_all_users)
    app.cli.add_command(update_targets)
