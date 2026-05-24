import sqlite3
import os

# =========================
# DATABASE PATH
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(
    BASE_DIR,
    "school.db"
)

# =========================
# CONNECT DATABASE
# =========================
conn = sqlite3.connect(db_path)

cursor = conn.cursor()

# =========================
# CREATE ALERTS TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS alerts (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_name TEXT NOT NULL,

    alert_type TEXT NOT NULL,

    message TEXT NOT NULL,

    created_at TEXT NOT NULL
)
""")

conn.commit()

conn.close()

print("✅ alerts table created successfully")
