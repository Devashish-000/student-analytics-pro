import sqlite3
import os

# =========================
# DATABASE PATH
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(BASE_DIR, "school.db")

# =========================
# CONNECT DATABASE
# =========================
conn = sqlite3.connect(db_path)

cursor = conn.cursor()

# =========================
# CREATE FEES TABLE
# =========================
cursor.execute("""

CREATE TABLE IF NOT EXISTS fees (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_name TEXT NOT NULL,

    class TEXT NOT NULL,

    total_fees REAL NOT NULL,

    paid_amount REAL NOT NULL,

    pending_amount REAL NOT NULL,

    due_date TEXT,

    status TEXT

)

""")

conn.commit()

conn.close()

print("✅ fees table created successfully")
