import time
import pandas as pd
import sqlite3
import os

def get_live_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.abspath(os.path.join(BASE_DIR, "../../database/school.db"))

    conn = sqlite3.connect(db_path)

    query = """
    SELECT
        s.id,
        s.name,
        s.class,
        COALESCE(m.maths, 0) as maths,
        COALESCE(m.physics, 0) as physics,
        COALESCE(m.chemistry, 0) as chemistry,
        COALESCE(m.english, 0) as english,
        COALESCE(a.attendance_percent, 0) as attendance
    FROM students s
    LEFT JOIN marks m ON s.id = m.student_id
    LEFT JOIN attendance a ON s.id = a.student_id
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df


def live_stream(interval=5):
    """Simulated WebSocket stream"""
    while True:
        yield get_live_data()
        time.sleep(interval)
