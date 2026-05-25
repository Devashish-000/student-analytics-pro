import sqlite3
import random

conn = sqlite3.connect("school.db")
cur = conn.cursor()

names = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun",
    "Sai", "Krishna", "Ishaan", "Rohan", "Kunal",
    "Rahul", "Aman", "Dev", "Karan", "Manav",
    "Darshan", "Prince", "Amit", "Nikhil", "Soham",
    "Ritesh", "Yash", "Om", "Jay", "Harsh",
    "Ravi", "Suresh", "Piyush", "Mihir", "Nirav",
    "Ankit", "Bhavik", "Chirag", "Deep", "Eshan",
    "Faiz", "Gaurav", "Hemant", "Irfan", "Jatin",
    "Kishan", "Lalit", "Mayur", "Nayan", "Omkar",
    "Parth", "Qasim", "Rajan", "Sanjay", "Tejas"
]

classes = ["8A", "8B", "9A", "9B", "10A", "10B", "11A", "11B", "12A"]

for i in range(50):
    name = names[i]
    cls = random.choice(classes)
    age = random.randint(14, 18)

    cur.execute("""
        INSERT INTO students (name, class, age)
        VALUES (?, ?, ?)
    """, (name, cls, age))

conn.commit()
conn.close()

print("✅ 50 students added successfully!")
