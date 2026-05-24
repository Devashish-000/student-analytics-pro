import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "../database/school.db")


def get_connection():
    return sqlite3.connect(db_path, check_same_thread=False)


# =========================
# CREATE STUDENT
# =========================
def add_student(name, class_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO students (name, class) VALUES (?, ?)",
        (name, class_name)
    )

    conn.commit()
    conn.close()


# =========================
# READ STUDENTS
# =========================
def get_students():
    conn = get_connection()
    df = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return df


# =========================
# UPDATE STUDENT
# =========================
def update_student(student_id, name, class_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE students SET name=?, class=? WHERE id=?",
        (name, class_name, student_id)
    )

    conn.commit()
    conn.close()


# =========================
# DELETE STUDENT
# =========================
def delete_student(student_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM students WHERE id=?", (student_id,))

    conn.commit()
    conn.close()
