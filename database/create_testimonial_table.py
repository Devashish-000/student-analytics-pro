import sqlite3

# Database connect
conn = sqlite3.connect("database/school.db")

cursor = conn.cursor()

# Create testimonials table
cursor.execute("""
CREATE TABLE IF NOT EXISTS testimonials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    rating INTEGER,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("✅ Testimonials table created successfully!")
