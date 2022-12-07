import importlib.resources
import os

import click

from .database import get_db_cm


@click.group()
def cli():
    pass


@cli.command()
def start():
    os.system("poetry run uvicorn --reload backend.main:app")


@cli.command()
def init_db():
    with importlib.resources.open_text("backend", "schema.sql") as s:
        with get_db_cm() as db:
            db.executescript(s.read())


if __name__ == "__main__":
    cli()
