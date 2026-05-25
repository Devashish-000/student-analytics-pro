import sqlite3

conn = sqlite3.connect("database/school.db")

cursor = conn.cursor()

# =========================
# CREATE TEACHER TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# =========================
# INSERT DEFAULT TEACHER
# =========================
cursor.execute("""
INSERT OR IGNORE INTO teachers
(username, password)
VALUES
('himani', '1234')
""")

conn.commit()

print("✅ Teacher table created successfully!")

conn.close()

