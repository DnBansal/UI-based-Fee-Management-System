# admin.py
# Database creation and admin password helpers (uses SHA-256 hashing).
import mysql.connector
from mysql.connector import Error
import hashlib

DB_NAME = "fee_structure"

def _hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

def create_db_if_missing():
    """
    Ensure the database and core tables exist. Creates a default hashed admin password 'qwaszx'
    if the pw table is empty.
    """
    try:
        # connect without database to check/create DB
        conn = mysql.connector.connect(host='localhost', user='root')
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        dbs = [d[0] for d in cursor.fetchall()]
        if DB_NAME not in dbs:
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
        cursor.close()
        conn.close()

        # connect with DB to create tables
        conn = mysql.connector.connect(host='localhost', user='root', database=DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS class (
            cid INT PRIMARY KEY AUTO_INCREMENT,
            cname VARCHAR(8),
            sec CHAR(1),
            tname VARCHAR(100)
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS fee (
            fid INT PRIMARY KEY AUTO_INCREMENT,
            cid INT,
            stu INT,
            date DATE,
            sf INT,
            lsf INT,
            tsf INT,
            vvn INT,
            lvvn INT,
            tvvn INT,
            cf INT,
            gt INT
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS pw (
            pw_hash VARCHAR(128)
        )""")

        cursor.execute("SELECT COUNT(*) FROM pw")
        cnt = cursor.fetchone()[0]
        if cnt == 0:
            default = _hash_password('qwaszx')
            cursor.execute("INSERT INTO pw (pw_hash) VALUES (%s)", (default,))

        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        # Re-raise to let caller handle UI-level messages or logging
        raise

def verify_password(plain_pw: str) -> bool:
    conn = mysql.connector.connect(host='localhost', user='root', database=DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT pw_hash FROM pw LIMIT 1")
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if not row:
        return False
    return _hash_password(plain_pw) == row[0]

def change_password(new_pw: str):
    h = _hash_password(new_pw)
    conn = mysql.connector.connect(host='localhost', user='root', database=DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE pw SET pw_hash = %s", (h,))
    conn.commit()
    cursor.close()
    conn.close()

def drop_database():
    conn = mysql.connector.connect(host='localhost', user='root')
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
    cursor.close()
    conn.close()
