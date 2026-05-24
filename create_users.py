import sqlite3
from app.utils.security import hash_password


conn = sqlite3.connect("database/school.db")

cursor = conn.cursor()


users = [
    ("admin", hash_password("Admin@123"), "admin"),
    ("rahul", hash_password("Rahul@123"), "student"),
    ("aman", hash_password("Aman@123"), "student"),
    ("dev", hash_password("Dev@123"), "student")
]


cursor.executemany(
    "INSERT INTO users VALUES (?, ?, ?)",
    users
)

conn.commit()

print("✅ Secure users added")
