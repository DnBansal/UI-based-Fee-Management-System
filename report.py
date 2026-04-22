# report.py
# Simple reporting helper(s)
import mysql.connector
from datetime import datetime

DB_NAME = "fee_structure"

def fees_on_date(date_str: str):
    """
    Returns rows of fees on exact date. Accepts dd-mm-yyyy or yyyy-mm-dd.
    """
    try:
        if '-' in date_str and len(date_str.split('-')[0]) == 4:
            dt = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            dt = datetime.strptime(date_str, '%d-%m-%Y').date()
    except Exception:
        raise
    conn = mysql.connector.connect(host='localhost', user='root', database=DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT fid, cid, stu, date, gt FROM fee WHERE date=%s", (dt,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
