# db.py
# Simple central DB helper (context manager). Edit DB_CONFIG if you need a password.
import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    # "password": "your_mysql_password_here",  # uncomment and set if needed
    "database": "fee_structure"
}

@contextmanager
def get_connection(with_database=True):
    """
    Context manager to acquire and close a MySQL connection.
    If with_database is False, the DB name will not be provided (useful for CREATE DATABASE).
    """
    cfg = DB_CONFIG.copy()
    if not with_database:
        cfg.pop("database", None)
    conn = None
    try:
        conn = mysql.connector.connect(**cfg)
        yield conn
    finally:
        if conn and conn.is_connected():
            conn.close()
