import streamlit as st
import sqlite3
import pandas as pd
import os

def show_student_profile(student_id):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "../database/school.db")

    conn = sqlite3.connect(db_path)

    query = """
    SELECT
        students.id,
        students.name,
        students.class,
        marks.maths,
        marks.physics,
        marks.chemistry,
        marks.english,
        attendance.attendance_percent
    FROM students
    JOIN marks ON students.id = marks.student_id
    JOIN attendance ON students.id = attendance.student_id
    WHERE students.id = ?
    """

    df = pd.read_sql_query(query, conn, params=(student_id,))
    conn.close()

    if df.empty:
        st.error("Student not found ❌")
        return

    student = df.iloc[0]

    total = student["maths"] + student["physics"] + student["chemistry"] + student["english"]
    avg = total / 4

    st.title(f"👤 {student['name']} Profile")

    st.metric("Class", student["class"])
    st.metric("Total Marks", total)
    st.metric("Average", round(avg, 2))
    st.metric("Attendance %", student["attendance_percent"])

    if avg >= 75:
        st.success("🔥 Excellent Performance")
    elif avg >= 50:
        st.warning("⚠ Average Performance")
    else:
        st.error("❌ Weak Performance")
