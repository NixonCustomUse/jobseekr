import sqlite3
import os

from config import DATABASE_PATH, BASE_DIR


def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    schema_path = os.path.join(BASE_DIR, "models", "schema.sql")
    with open(schema_path) as f:
        schema = f.read()
    conn = get_db()
    conn.executescript(schema)
    conn.commit()
    conn.close()


def query(sql, params=None):
    conn = get_db()
    cur = conn.execute(sql, params or [])
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return [dict(r) for r in rows]


def query_one(sql, params=None):
    rows = query(sql, params)
    return rows[0] if rows else None


def execute(sql, params=None):
    conn = get_db()
    cur = conn.execute(sql, params or [])
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id
