import streamlit as st
import sqlite3
import pandas as pd
import os

from app.utils.ai_engine import predict_grade


def profile_page():

    # =====================================
    # PAGE TITLE
    # =====================================
    st.title("🧑‍🎓 Student Profile")

    st.caption(
        "AI Powered Student Profile System"
    )

    # =====================================
    # SESSION DATA
    # =====================================
    user = st.session_state.get("user")

    role = st.session_state.get("role")

    # =====================================
    # DATABASE CONNECTION
    # =====================================
    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    db_path = os.path.join(
        BASE_DIR,
        "../database/school.db"
    )

    conn = sqlite3.connect(db_path)

    # =====================================
    # SQL QUERY
    # =====================================
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

    JOIN marks
        ON students.id = marks.student_id

    JOIN attendance
        ON students.id = attendance.student_id
    """

    # =====================================
    # LOAD DATA
    # =====================================
    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    # =====================================
    # EMPTY CHECK
    # =====================================
    if df.empty:

        st.warning(
            "❌ No profile data found"
        )

        return

    # =====================================
    # CLEAN DATA
    # =====================================
    df = df.fillna(0)

    # =====================================
    # ROLE FILTER
    # =====================================
    if role == "student" and user:

        df = df[
            df["name"]
            .str.lower()
            == user.lower()
        ]

    # =====================================
    # PROFILE CHECK
    # =====================================
    if df.empty:

        st.error(
            "❌ Profile not found"
        )

        return

    # =====================================
    # SELECT STUDENT
    # =====================================
    student = df.iloc[0]

    # =====================================
    # MARKS CALCULATION
    # =====================================
    total = (
        student["maths"]
        + student["physics"]
        + student["chemistry"]
        + student["english"]
    )

    average = total / 4

    # =====================================
    # AI ENGINE
    # =====================================
    result, ai_score = predict_grade(
        average,
        student["attendance_percent"]
    )

    # =====================================
    # PROFILE PHOTO
    # =====================================
    st.subheader("📸 Profile Photo")

    uploaded_file = st.file_uploader(
        "Upload Your Photo",
        type=[
            "png",
            "jpg",
            "jpeg"
        ]
    )

    # =====================================
    # UPLOAD FOLDER
    # =====================================
    upload_dir = os.path.join(
        BASE_DIR,
        "..",
        "uploads"
    )

    # CREATE FOLDER
    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    # IMAGE PATH
    image_path = os.path.join(
        upload_dir,
        f"{student['name']}.png"
    )

    # =====================================
    # SAVE IMAGE
    # =====================================
    if uploaded_file:

        with open(
            image_path,
            "wb"
        ) as f:

            f.write(
                uploaded_file.getbuffer()
            )

        st.success(
            "✅ Photo Uploaded Successfully"
        )

    # =====================================
    # PROFILE CARD
    # =====================================
    st.divider()

    col1, col2 = st.columns([1, 3])

    # =====================================
    # IMAGE SECTION
    # =====================================
    with col1:

        if os.path.exists(image_path):

            st.image(
                image_path,
                width=180
            )

        else:

            st.info(
                "📷 No Image Uploaded"
            )

    # =====================================
    # DETAILS SECTION
    # =====================================
    with col2:

        st.subheader(
            f"👤 {student['name']}"
        )

        st.write(
            f"📚 Class: {student['class']}"
        )

        st.write(
            f"📊 Attendance: {student['attendance_percent']}%"
        )

        st.write(
            f"🤖 AI Result: {result}"
        )

        st.write(
            f"🧠 AI Score: {round(ai_score, 2)}"
        )

    st.divider()

    # =====================================
    # PERFORMANCE OVERVIEW
    # =====================================
    st.subheader(
        "📊 Performance Overview"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🏆 Total Marks",
        int(total)
    )

    col2.metric(
        "📈 Average",
        round(average, 2)
    )

    col3.metric(
        "🤖 AI Result",
        result
    )

    col4.metric(
        "🧠 AI Score",
        round(ai_score, 2)
    )

    st.divider()

    # =====================================
    # SUBJECT WISE MARKS
    # =====================================
    st.subheader(
        "📚 Subject Wise Marks"
    )

    marks_df = pd.DataFrame({

        "Subject": [
            "Maths",
            "Physics",
            "Chemistry",
            "English"
        ],

        "Marks": [
            student["maths"],
            student["physics"],
            student["chemistry"],
            student["english"]
        ]
    })

    st.dataframe(
        marks_df,
        use_container_width=True
    )

    st.divider()

    # =====================================
    # PERFORMANCE MESSAGE
    # =====================================
    if ai_score >= 80:

        st.success(
            "🌟 Excellent Performance"
        )

    elif ai_score >= 60:

        st.info(
            "👍 Good Performance"
        )

    else:

        st.warning(
            "⚠ Needs Improvement"
        )

    st.divider()

    # =====================================
    # FOOTER
    # =====================================
    st.caption(
        "🚀 AI Powered Student Profile"
    )
