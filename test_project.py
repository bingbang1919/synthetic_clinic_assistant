import unittest
import sqlite3
from pathlib import Path
from database import run_query
class DatabaseTests(unittest.TestCase):
    def test_patient_count(self):
        self.assertEqual(run_query('SELECT COUNT(*) FROM patient')['rows'],[[100]])
    def test_visit_count(self):
        self.assertEqual(run_query('SELECT COUNT(*) FROM visit')['rows'],[[500]])
    def test_foreign_keys(self):
        con=sqlite3.connect(Path(__file__).resolve().parent/'clinic.db')
        try:
            self.assertEqual(con.execute('PRAGMA foreign_key_check').fetchall(),[])
        finally:
            con.close()
    def test_no_visit_patients(self):
        r=run_query('SELECT COUNT(*) FROM patient p WHERE NOT EXISTS (SELECT 1 FROM visit v WHERE v.patient_id=p.patient_id)')
        self.assertGreaterEqual(r['rows'][0][0],10)
    def test_cte(self):
        self.assertEqual(run_query('WITH t AS (SELECT patient_id FROM patient) SELECT COUNT(*) FROM t')['rows'],[[100]])
    def test_truncation(self):
        r=run_query('SELECT visit_id FROM visit')
        self.assertTrue(r['truncated'])
        self.assertEqual(len(r['rows']),200)
    def test_blocked_queries(self):
        for sql in ['DELETE FROM patient','DROP TABLE patient','PRAGMA table_info(patient)',
                    'SELECT * FROM sqlite_master',"SELECT load_extension('anything')",
                    'SELECT 1; DELETE FROM patient;',
                    'WITH x AS (SELECT 1) DELETE FROM patient']:
            with self.subTest(sql=sql):
                with self.assertRaises((ValueError,sqlite3.Error)):
                    run_query(sql)
if __name__ == '__main__':
    unittest.main()
