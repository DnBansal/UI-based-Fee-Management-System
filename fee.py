# fee.py
# Fee operations: add fee record, query by class
import mysql.connector
from mysql.connector import Error
from datetime import datetime

DB_NAME = "fee_structure"

def _to_sql_date(d_str: str):
    """
    Accepts 'dd-mm-yyyy' or 'yyyy-mm-dd' and returns a datetime.date.
    Raises ValueError on bad format.
    """
    try:
        if '-' in d_str and len(d_str.split('-')[0]) == 4:
            dt = datetime.strptime(d_str, '%Y-%m-%d')
        else:
            dt = datetime.strptime(d_str, '%d-%m-%Y')
        return dt.date()
    except ValueError:
        raise

def add_fee(cid:int, stu:int, date_str:str, sf:int, lsf:int, tsf:int,
            vvn:int, lvvn:int, tvvn:int, cf:int, gt:int):
    date_sql = _to_sql_date(date_str)
    conn = mysql.connector.connect(host='localhost', user='root', database=DB_NAME)
    cur = conn.cursor()
    cur.execute("""INSERT INTO fee (cid, stu, date, sf, lsf, tsf, vvn, lvvn, tvvn, cf, gt)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (cid, stu, date_sql, sf, lsf, tsf, vvn, lvvn, tvvn, cf, gt))
    conn.commit()
    cur.close()
    conn.close()
    return True

def get_fees_by_class(cid:int):
    conn = mysql.connector.connect(host='localhost', user='root', database=DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT fid, cid, stu, date, gt FROM fee WHERE cid=%s ORDER BY date", (cid,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
