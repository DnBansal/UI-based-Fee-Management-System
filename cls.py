# cls.py
# Class management functions (get classes, add class, find class id)
import mysql.connector
from mysql.connector import Error

DB_NAME = "fee_structure"

def get_all_classes():
    conn = mysql.connector.connect(host='localhost', user='root', database=DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT cid, cname, sec, tname FROM class ORDER BY cid")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def add_class(cname: str, sec: str, tname: str = ""):
    conn = mysql.connector.connect(host='localhost', user='root', database=DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO class (cname, sec, tname) VALUES (%s, %s, %s)", (cname, sec, tname))
    conn.commit()
    cur.close()
    conn.close()
    return True

def find_class_id(cname: str, sec: str):
    conn = mysql.connector.connect(host='localhost', user='root', database=DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT cid FROM class WHERE cname=%s AND sec=%s LIMIT 1", (cname, sec))
    r = cur.fetchone()
    cur.close()
    conn.close()
    return r[0] if r else None
