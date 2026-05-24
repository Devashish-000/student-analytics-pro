from utils.notifications import (
    low_attendance_alert,
    low_marks_alert,
    marks_drop_alert,
    warning_students
)

import streamlit as st
import sqlite3
import pandas as pd
import os

# =========================
# PDF IMPORTS
# =========================
from reportlab.pdfgen import canvas
from io import BytesIO

# =========================
# AI MODULES (FIXED IMPORTS)
# =========================
from ai.ai_engine import analyze_data, predict_grade
from ai.ai_insights import show_ai_insights

# =========================
# CHARTS
# =========================
from charts.bar_chart import show_bar_chart
from charts.pie_chart import show_pie_chart
from charts.attendance_chart import show_attendance_chart

# =========================
# CHATBOT (SAFE IMPORT)
# =========================
from chatbot import chatbot


def show_dashboard():

    st.title("🎓 Student Analytics System")
    st.caption("🤖 AI Powered Performance Dashboard")

    # =========================
    # DATABASE
    # =========================
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
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        st.warning("❌ No data found in database")
        return

    # =========================
    # CLEAN DATA
    # =========================
    df = df.drop_duplicates(subset=["id"]).fillna(0).reset_index(drop=True)

    df.rename(columns={"attendance_percent": "attendance"}, inplace=True)

    # =========================
    # CALCULATIONS
    # =========================
    df["Total"] = df[["maths", "physics", "chemistry", "english"]].sum(axis=1)
    df["Average"] = df["Total"] / 4

    # =========================
    # AI PREDICTION
    # =========================
    results = df.apply(
        lambda row: predict_grade(row["Average"], row["attendance"]),
        axis=1
    )

    df["AI_Result"] = results.apply(lambda x: x[0])
    df["AI_Score"] = results.apply(lambda x: x[1])

    # =========================
    # SESSION
    # =========================
    role = st.session_state.get("role", "student")
    user = st.session_state.get("user", None)

    table_df = df.copy()

    if role == "student" and user:
        table_df = table_df[
            table_df["name"].str.lower() == user.lower()
        ]

    # =========================
    # SIDEBAR
    # =========================
    st.sidebar.title("⚙ Control Panel")

    classes = ["All Classes"] + sorted(df["class"].unique().tolist())

    selected_class = st.sidebar.selectbox("📚 Select Class", classes)
    search = st.sidebar.text_input("🔍 Search Student")

    st.sidebar.info(f"👤 User: {user}")
    st.sidebar.info(f"🔐 Role: {role}")

    filtered = table_df.copy()

    if selected_class != "All Classes":
        filtered = filtered[filtered["class"] == selected_class]

    if search:
        filtered = filtered[
            filtered["name"].str.lower().str.contains(search.lower(), na=False)
        ]

    # =========================
    # KPI
    # =========================
    st.subheader("📊 Dashboard Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👨‍🎓 Students", len(df))
    col2.metric("📈 Avg Marks", round(df["Average"].mean(), 2))
    col3.metric("🏆 Top Score", int(df["Total"].max()))
    col4.metric("⚠ Weak Students", len(df[df["AI_Score"] < 60]))

    st.divider()

    # =========================
    # TABLE
    # =========================
    st.subheader("📚 Students Data")
    st.dataframe(filtered, use_container_width=True)

    st.divider()

    # =========================
    # WEAK STUDENTS
    # =========================
    st.subheader("⚠ Weak Students Alert")

    weak = df[df["AI_Score"] < 60]

    if weak.empty:
        st.success("No weak students detected 🚀")
    else:
        st.warning(f"⚠ {len(weak)} Weak Students Found!")
        st.dataframe(
            weak[["name", "class", "Average", "attendance", "AI_Score"]],
            use_container_width=True
        )

    st.divider()

    # =========================
    # NOTIFICATIONS
    # =========================
    st.subheader("🔔 Smart Notifications System")

    att_alerts = low_attendance_alert(df)
    marks_alerts = low_marks_alert(df)
    warn = warning_students(df)
    drop = marks_drop_alert(df)

    if not att_alerts.empty:
        st.error(f"🚨 {len(att_alerts)} Students have low attendance!")
        st.dataframe(att_alerts)

    if not marks_alerts.empty:
        st.warning(f"📉 {len(marks_alerts)} Students need improvement!")
        st.dataframe(marks_alerts)

    if not warn.empty:
        st.info(f"🧑‍🏫 Warning Panel: {len(warn)} Students need attention")
        st.dataframe(warn)

    if not drop.empty:
        st.error("📉 Marks Drop Detected!")
        st.dataframe(drop)

    st.divider()

    # =========================
    # CHARTS
    # =========================
    st.subheader("📊 Analytics Dashboard")

    show_bar_chart(df)
    st.divider()

    show_attendance_chart(df)
    st.divider()

    show_pie_chart(df)

    st.divider()

    # =========================
    # CHATBOT
    # =========================
    st.subheader("🤖 AI Student Assistant")

    try:
        chatbot(df)
    except Exception:
        st.warning("Chatbot temporarily unavailable")

    st.divider()

    # =========================
    # PDF REPORT DOWNLOAD
    # =========================
    st.subheader("📄 Download Student Report")

    def generate_pdf(data):

        buffer = BytesIO()

        p = canvas.Canvas(buffer)

        y = 800

        p.setFont("Helvetica-Bold", 16)
        p.drawString(180, y, "Student Analytics Report")

        y -= 40

        p.setFont("Helvetica", 12)

        for index, row in data.iterrows():

            text = (
                f"Name: {row['name']} | "
                f"Class: {row['class']} | "
                f"Average: {round(row['Average'],2)} | "
                f"Attendance: {row['attendance']}% | "
                f"AI Grade: {row['AI_Result']}"
            )

            p.drawString(40, y, text)

            y -= 25

            if y < 50:
                p.showPage()
                y = 800

        p.save()

        buffer.seek(0)

        return buffer

    pdf_file = generate_pdf(filtered)

    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_file,
        file_name="student_report.pdf",
        mime="application/pdf"
    )

    st.divider()

    st.caption("🚀 Built with Streamlit | AI Student Intelligence System")
