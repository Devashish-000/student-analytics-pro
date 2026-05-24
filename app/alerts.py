import streamlit as st
import sqlite3
import pandas as pd
import os

from datetime import datetime


def alerts_page():

    st.title("📱 SMS / WhatsApp Alerts")

    # =========================
    # DATABASE
    # =========================
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    db_path = os.path.join(
        BASE_DIR,
        "../database/school.db"
    )

    conn = sqlite3.connect(db_path)

    role = st.session_state.get("role")
    user = st.session_state.get("user")

    # =========================
    # ADMIN PANEL
    # =========================
    if role == "admin":

        st.subheader("📨 Send Alert")

        student_name = st.text_input(
            "👨‍🎓 Student Name"
        )

        alert_type = st.selectbox(
            "📢 Alert Type",
            [
                "SMS Alert",
                "WhatsApp Alert",
                "Fee Reminder",
                "Attendance Warning"
            ]
        )

        message = st.text_area(
            "✍ Alert Message"
        )

        # =========================
        # SEND ALERT
        # =========================
        if st.button("🚀 Send Alert"):

            current_time = datetime.now().strftime(
                "%d %b %Y | %I:%M %p"
            )

            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO alerts (
                    student_name,
                    alert_type,
                    message,
                    created_at
                )

                VALUES (?, ?, ?, ?)
                """,
                (
                    student_name,
                    alert_type,
                    message,
                    current_time
                )
            )

            conn.commit()

            st.success("✅ Alert Sent Successfully")

    st.divider()

    # =========================
    # SHOW ALERTS
    # =========================
    st.subheader("📨 Alerts Inbox")

    query = """
    SELECT * FROM alerts
    ORDER BY id DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    # =========================
    # EMPTY CHECK
    # =========================
    if df.empty:

        st.warning("No alerts available")

        return

    # =========================
    # STUDENT VIEW
    # =========================
    if role == "student":

        df = df[
            df["student_name"].str.lower()
            ==
            str(user).lower()
        ]

    # =========================
    # DISPLAY ALERTS
    # =========================
    for _, row in df.iterrows():

        with st.container():

            st.markdown(f"""
            ### 📢 {row['alert_type']}

            👨‍🎓 Student: {row['student_name']}

            💬 Message:
            {row['message']}

            🕒 {row['created_at']}
            """)

            st.divider()
