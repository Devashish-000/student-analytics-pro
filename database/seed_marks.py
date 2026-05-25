import sqlite3
import random

conn = sqlite3.connect("school.db")
cur = conn.cursor()

cur.execute("SELECT id FROM students")
students = cur.fetchall()

for s in students:
    sid = s[0]

    maths = random.randint(40, 95)
    physics = random.randint(40, 95)
    chemistry = random.randint(40, 95)
    english = random.randint(40, 95)

    cur.execute("""
        INSERT OR REPLACE INTO marks
        (student_id, maths, physics, chemistry, english)
        VALUES (?, ?, ?, ?, ?)
    """, (sid, maths, physics, chemistry, english))

conn.commit()
conn.close()

print("✅ Marks inserted successfully for all students!")
