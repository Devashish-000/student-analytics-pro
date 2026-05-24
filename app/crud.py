import streamlit as st
import sqlite3
import os
import pandas as pd

# =========================
# DB CONNECTION
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "../database/school.db")

conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()


# =========================
# CRUD PAGE
# =========================
def crud_page():

    st.title("🧑‍🎓 Student Management System (CRUD)")

    menu = st.sidebar.radio(
        "Select Action",
        ["View", "Add", "Update", "Delete"]
    )

    # ================= VIEW =================
    if menu == "View":

        st.subheader("📋 All Students")

        df = pd.read_sql_query("SELECT * FROM students", conn)
        st.dataframe(df, use_container_width=True)


    # ================= ADD =================
    elif menu == "Add":

        st.subheader("➕ Add Student")

        name = st.text_input("Name")
        class_name = st.text_input("Class")
        age = st.number_input("Age", min_value=1, max_value=100, step=1)

        if st.button("Add Student"):

            if not name or not class_name or not age:
                st.warning("Please fill all fields ❗")
                return

            try:
                cursor.execute(
                    "INSERT INTO students (name, class, age) VALUES (?, ?, ?)",
                    (name, class_name, int(age))
                )
                conn.commit()
                st.success("Student Added Successfully 🚀")

            except Exception as e:
                st.error(f"Error: {e}")


    # ================= UPDATE =================
    elif menu == "Update":

        st.subheader("✏ Update Student")

        sid = st.number_input("Student ID", step=1)
        name = st.text_input("New Name")
        class_name = st.text_input("New Class")
        age = st.number_input("New Age", min_value=1, max_value=100, step=1)

        if st.button("Update Student"):

            if sid == 0:
                st.warning("Enter valid Student ID ❗")
                return

            try:
                cursor.execute(
                    "UPDATE students SET name=?, class=?, age=? WHERE id=?",
                    (name, class_name, int(age), int(sid))
                )
                conn.commit()
                st.success("Student Updated Successfully 🚀")

            except Exception as e:
                st.error(f"Error: {e}")


    # ================= DELETE =================
    elif menu == "Delete":

        st.subheader("❌ Delete Student")

        sid = st.number_input("Student ID", step=1)

        if st.button("Delete Student"):

            if sid == 0:
                st.warning("Enter valid Student ID ❗")
                return

            try:
                cursor.execute(
                    "DELETE FROM students WHERE id=?",
                    (int(sid),)
                )
                conn.commit()
                st.warning("Student Deleted ⚠")

            except Exception as e:
                st.error(f"Error: {e}")
