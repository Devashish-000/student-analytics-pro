import streamlit as st
import pandas as pd
from models.student_model import (
    add_student,
    get_students,
    update_student,
    delete_student
)

# =========================
# STUDENT CRUD PAGE
# =========================
def show_students_page():

    st.title("👨‍🎓 Students CRUD System")

    menu = st.sidebar.selectbox(
        "📌 Menu",
        ["View", "Add", "Update", "Delete"]
    )

    # =========================
    # VIEW STUDENTS
    # =========================
    if menu == "View":
        data = get_students()
        df = pd.DataFrame(data, columns=["ID", "Name", "Class"])
        st.dataframe(df, use_container_width=True)

    # =========================
    # ADD STUDENT
    # =========================
    elif menu == "Add":
        st.subheader("➕ Add Student")

        name = st.text_input("Student Name")
        class_name = st.text_input("Class")

        if st.button("Add Student"):
            add_student(name, class_name)
            st.success("Student Added Successfully 🚀")
            st.rerun()

    # =========================
    # UPDATE STUDENT
    # =========================
    elif menu == "Update":
        st.subheader("✏ Update Student")

        student_id = st.number_input("Student ID", min_value=1)
        name = st.text_input("New Name")
        class_name = st.text_input("New Class")

        if st.button("Update Student"):
            update_student(student_id, name, class_name)
            st.success("Student Updated Successfully 🚀")
            st.rerun()

    # =========================
    # DELETE STUDENT
    # =========================
    elif menu == "Delete":
        st.subheader("❌ Delete Student")

        student_id = st.number_input("Student ID", min_value=1)

        if st.button("Delete Student"):
            delete_student(student_id)
            st.success("Student Deleted Successfully 🚀")
            st.rerun()
