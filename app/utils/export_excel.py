import pandas as pd
import sqlite3
import os

def export_excel():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "../../database/school.db")

    conn = sqlite3.connect(db_path)

    df = pd.read_sql_query("SELECT * FROM students", conn)

    file_path = "students_report.xlsx"
    df.to_excel(file_path, index=False)

    return file_path
