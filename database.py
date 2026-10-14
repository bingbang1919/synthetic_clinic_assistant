from pathlib import Path
import sqlite3
import time
BASE = Path(__file__).resolve().parent
TABLES = {'patient','provider','visit','condition','patient_condition','medication','prescription'}
FUNCTIONS = {'count','sum','avg','min','max','round','abs','coalesce','ifnull','nullif',
 'date','datetime','strftime','julianday','substr','lower','upper','length','trim',
 'like','glob','total','group_concat','row_number','rank','dense_rank'}
MAX_ROWS = 200

def get_schema():
    return (BASE / 'schema.sql').read_text()

def run_query(sql):
    if not isinstance(sql,str) or not sql.strip():
        raise ValueError('SQL is empty.')
    sql = sql.strip()
    if len(sql)>12000 or sql.split(None,1)[0].upper() not in {'SELECT','WITH'}:
        raise ValueError('Only a SELECT query or read-only WITH query is allowed.')
    path = BASE / 'clinic.db'
    con = sqlite3.connect(path.as_uri()+'?mode=ro',uri=True)
    con.execute('PRAGMA query_only = ON')
    def authorize(action,a,b,db,source):
        if action in (sqlite3.SQLITE_SELECT,sqlite3.SQLITE_RECURSIVE):
            return sqlite3.SQLITE_OK
        if action == sqlite3.SQLITE_READ and a in TABLES and db in ('main', None):
            return sqlite3.SQLITE_OK
        if action == sqlite3.SQLITE_FUNCTION and (b or a or '').lower() in FUNCTIONS:
            return sqlite3.SQLITE_OK
        return sqlite3.SQLITE_DENY
    con.set_authorizer(authorize)
    started=time.monotonic()
    con.set_progress_handler(lambda: int(time.monotonic()-started>3),1000)
    try:
        cur=con.execute(sql)
        columns=[d[0] for d in cur.description]
        rows=cur.fetchmany(MAX_ROWS+1)
        truncated=len(rows)>MAX_ROWS
        return {'columns':columns,'rows':[list(r) for r in rows[:MAX_ROWS]],'truncated':truncated,'row_limit':MAX_ROWS}
    finally:
        con.close()
