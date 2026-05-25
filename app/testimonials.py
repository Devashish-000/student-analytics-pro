import streamlit as st
import sqlite3
import pandas as pd
import os


# =========================
# DATABASE PATH
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.abspath(os.path.join(BASE_DIR, "../database/school.db"))


# =========================
# SAVE TESTIMONIAL
# =========================
def save_testimonial(name, rating, message):

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO testimonials (student_name, rating, message)
        VALUES (?, ?, ?)
    """, (name, rating, message))

    conn.commit()
    conn.close()


# =========================
# GET TESTIMONIALS
# =========================
def get_testimonials():

    conn = sqlite3.connect(db_path)

    df = pd.read_sql_query("""
        SELECT * FROM testimonials
        ORDER BY id DESC
    """, conn)

    conn.close()

    return df


# =========================
# MAIN UI
# =========================
def show_testimonials():

    st.markdown("## 💬 Student Testimonials")

    st.caption("Students can share feedback and messages with admin")

    # =========================
    # FORM
    # =========================
    with st.form("testimonial_form"):

        student_name = st.text_input("👤 Your Name")

        rating = st.slider("⭐ Rating", 1, 5, 5)

        message = st.text_area(
            "💬 Your Message",
            placeholder="Write your feedback here..."
        )

        submitted = st.form_submit_button("🚀 Submit Feedback")

        if submitted:

            if student_name and message:

                save_testimonial(student_name, rating, message)

                st.success("✅ Feedback Submitted Successfully!")

            else:
                st.warning("⚠ Please fill all fields")

    st.markdown("---")

    # =========================
    # SHOW TESTIMONIALS
    # =========================
    testimonials = get_testimonials()

    if testimonials.empty:

        st.info("No testimonials yet")

    else:

        for _, row in testimonials.iterrows():

            stars = "⭐" * int(row["rating"])

            st.markdown(
                f"""
                <div style="
                    background:#111827;
                    padding:15px;
                    border-radius:12px;
                    margin-bottom:10px;
                    border:1px solid #374151;
                ">

                <h4 style="margin:0;">
                    👤 {row['student_name']}
                </h4>

                <p style="margin:5px 0;">
                    {stars}
                </p>

                <p style="color:#d1d5db;">
                    {row['message']}
                </p>

                <small style="color:gray;">
                    🕒 {row['created_at']}
                </small>

                </div>
                """,
                unsafe_allow_html=True
            )
