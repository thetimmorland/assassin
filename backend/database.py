import importlib.resources
import sqlite3
from contextlib import contextmanager

import aiosql

from .config import get_settings


def get_db():
    db = sqlite3.connect(get_settings().db_path, check_same_thread=False)
    db.row_factory = sqlite3.Row
    try:
        yield db
    finally:
        db.close()


get_db_cm = contextmanager(get_db)


queries = aiosql.from_path(
    importlib.resources.path("backend", "queries.sql"), "sqlite3"
)
