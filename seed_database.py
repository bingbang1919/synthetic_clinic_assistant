from pathlib import Path
import sqlite3
import random
from datetime import date, timedelta
BASE = Path(__file__).resolve().parent
AS_OF = date(2026, 10, 13)
def seed():
    rng = random.Random(42)
    path = BASE / 'clinic.db'
    if path.exists():
        raise FileExistsError('clinic.db already exists. Delete it deliberately before reseeding.')
    con = sqlite3.connect(path)
    try:
        con.executescript((BASE / 'schema.sql').read_text())
        first = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Sam', 'Avery']
        last = ['Adams', 'Baker', 'Chen', 'Diaz', 'Evans', 'Flores', 'Green', 'Hall']
        for pid in range(1, 101):
            born = date(rng.randint(1940,2005),rng.randint(1,12),rng.randint(1,28))
            con.execute('INSERT INTO patient VALUES (?,?,?,?)',
                (pid,first[(pid-1)%8],last[((pid-1)//8)%8],born.isoformat()))
        for pid in range(1,9):
            con.execute('INSERT INTO provider VALUES (?,?,?)',
                (pid,f'Fictional Provider {pid}', ['Family Medicine','Internal Medicine','Endocrinology','Pulmonology'][(pid-1)%4]))
        conditions = ['Type 2 diabetes','Hypertension','Asthma','Hyperlipidemia','Hypothyroidism','Osteoarthritis','Migraine','Anxiety','GERD','Seasonal allergies']
        meds = ['Metformin','Lisinopril','Albuterol','Atorvastatin','Levothyroxine','Acetaminophen','Sumatriptan','Sertraline','Omeprazole','Cetirizine','Losartan','Amlodipine','Budesonide','Naproxen','Famotidine']
        con.executemany('INSERT INTO condition VALUES (?,?)',enumerate(conditions,1))
        con.executemany('INSERT INTO medication VALUES (?,?)',enumerate(meds,1))
        rxid = 0
        for pid in range(1,101):
            for cid in sorted(rng.sample(range(1,11),rng.randint(0,4))):
                diagnosis = AS_OF-timedelta(days=rng.randint(180,1500))
                con.execute('INSERT INTO patient_condition VALUES (?,?,?)',(pid,cid,diagnosis.isoformat()))
                if rng.random()<0.8:
                    rxid += 1
                    start = max(diagnosis,AS_OF-timedelta(days=rng.randint(30,700)))
                    end = (start+timedelta(days=30)).isoformat() if rng.random()<0.25 else None
                    con.execute('INSERT INTO prescription VALUES (?,?,?,?,?,?,?)',
                        (rxid,pid,cid,rng.randint(1,8),start.isoformat(),end,'Synthetic example dose; not clinical guidance'))
        for vid in range(1,501):
            con.execute('INSERT INTO visit VALUES (?,?,?,?,?)',
                (vid,rng.randint(1,90),rng.randint(1,8),(AS_OF-timedelta(days=rng.randint(0,1095))).isoformat(),rng.choice(['Routine','Follow-up','Urgent'])))
        con.commit()
        assert not con.execute('PRAGMA foreign_key_check').fetchall()
        print('Created clinic.db with 100 patients, 8 providers and 500 visits.')
    finally:
        con.close()
if __name__ == '__main__':
    seed()
