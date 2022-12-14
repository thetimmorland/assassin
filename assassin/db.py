import functools
import sqlite3

import aiosql
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource("sql/schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@functools.cache
def get_queries():
    with current_app.open_resource("sql/queries.sql") as f:
        return aiosql.from_str(f.read().decode("utf8"), "sqlite3")


class Queries:
    def __getattr__(self, name):
        return lambda db, *args, **kwargs: getattr(get_queries(), name)(
            db, *args, **kwargs
        )


queries = Queries()


def init_app(app):
    sqlite3.register_adapter(bool, int)
    sqlite3.register_converter("boolean", lambda v: bool(int(v)))
    app.teardown_appcontext(close_db)
