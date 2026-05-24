import streamlit as st
import sqlite3
import pandas as pd
import os


def ranking_page():

    st.title("🏆 Student Ranking System (Top 10 Leaderboard)")

    # =========================
    # DATABASE CONNECTION
    # =========================
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "../database/school.db")

    conn = sqlite3.connect(db_path)

    query = """
    SELECT
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
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    # =========================
    # SAFE CHECK
    # =========================
    if df.empty:
        st.warning("No data available ❗")
        return

    df = df.fillna(0)

    # =========================
    # TOTAL + AVERAGE
    # =========================
    df["Total"] = df[["maths", "physics", "chemistry", "english"]].sum(axis=1)
    df["Average"] = df["Total"] / 4

    # =========================
    # RANKING LOGIC
    # =========================
    df = df.sort_values(by="Total", ascending=False).reset_index(drop=True)
    df["Rank"] = df.index + 1

    top10 = df.head(10)

    # =========================
    # TOPPER HIGHLIGHT
    # =========================
    topper = top10.iloc[0]

    st.success(
        f"🏆 Topper: {topper['name']} | Class: {topper['class']} | Score: {topper['Total']}"
    )

    # =========================
    # LEADERBOARD TABLE
    # =========================
    st.subheader("🥇 Top 10 Leaderboard")

    st.dataframe(
        top10[["Rank", "name", "class", "Total", "Average", "attendance_percent"]],
        use_container_width=True
    )

    # =========================
    # CHART VIEW
    # =========================
    st.subheader("📊 Performance Chart")

    st.bar_chart(top10.set_index("name")["Total"])
