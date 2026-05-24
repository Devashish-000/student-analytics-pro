import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime


def notice_page():

    st.title("📢 Notice Board")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "../database/school.db")

    conn = sqlite3.connect(db_path)

    role = st.session_state.get("role")

    # =========================
    # ADMIN PANEL
    # =========================
    if role == "admin":

        st.subheader("✍ Create Notice")

        title = st.text_input("Notice Title")

        message = st.text_area("Notice Message")

        if st.button("📢 Publish Notice"):

            # =========================
            # DATE TIME FIX
            # =========================
            created_at = datetime.now().strftime(
                "%d %b %Y | %I:%M %p"
            )

            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO notices (
                    title,
                    message,
                    created_at
                )
                VALUES (?, ?, ?)
                """,
                (
                    title,
                    message,
                    created_at
                )
            )

            conn.commit()

            st.success("✅ Notice Published")

    st.divider()

    # =========================
    # SHOW NOTICES
    # =========================
    st.subheader("📄 Latest Notices")

    query = """
    SELECT * FROM notices
    ORDER BY id DESC
    """

    notices = pd.read_sql_query(query, conn)

    conn.close()

    if notices.empty:
        st.info("No notices available")
        return

    for _, row in notices.iterrows():

        with st.container():

            st.markdown(f"""
            ### 📌 {row['title']}

            {row['message']}

            🕒 {row['created_at']}
            """)

            st.divider()
