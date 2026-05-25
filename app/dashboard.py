from app.utils.notifications import (
    low_attendance_alert,
    low_marks_alert,
    marks_drop_alert,
    warning_students
)

from app.utils.live_notifications import (
    push_notification,
    get_notifications
)

import streamlit as st
import sqlite3
import pandas as pd
import os
from io import BytesIO
import time
import base64

from reportlab.pdfgen import canvas

from ai.ai_engine import predict_grade
from ai.ai_insights import show_ai_insights

from charts.bar_chart import show_bar_chart
from charts.pie_chart import show_pie_chart
from charts.attendance_chart import show_attendance_chart

from chatbot import chatbot


# =========================
# SAFE RERUN
# =========================
def safe_rerun():
    try:
        st.rerun()
    except:
        try:
            st.experimental_rerun()
        except:
            pass


# =========================
# 🔊 SOUND FUNCTION
# =========================
def play_notification_sound():
    try:
        audio_path = os.path.join("app", "assets", "notify.mp3")

        if os.path.exists(audio_path):
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()

            st.audio(audio_bytes, format="audio/mp3")
    except:
        pass


# =========================
# NOTIFICATION HELPER
# =========================
def notify_once(key, message, level="info"):
    if "notif_cache" not in st.session_state:
        st.session_state.notif_cache = set()

    if key not in st.session_state.notif_cache:
        push_notification(message, level)
        st.session_state.notif_cache.add(key)

        # 🔊 SOUND TRIGGER
        play_notification_sound()


# =========================
# MAIN DASHBOARD
# =========================
def show_dashboard():

    st.title("🎓 Student Analytics System")
    st.caption("🤖 AI Powered Performance Dashboard")

    # =========================
    # LIVE AUTO REFRESH
    # =========================
    refresh_time = st.sidebar.slider("⏱ Auto Refresh (seconds)", 0, 60, 0)

    if refresh_time > 0:
        st.info(f"🔄 Live Mode ON | Refresh every {refresh_time} seconds")
        time.sleep(refresh_time)
        safe_rerun()

    # =========================
    # DATABASE
    # =========================
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.abspath(os.path.join(BASE_DIR, "../database/school.db"))

    conn = sqlite3.connect(db_path)

    query = """
    SELECT
        s.id,
        s.name,
        s.class,
        COALESCE(m.maths, 0) as maths,
        COALESCE(m.physics, 0) as physics,
        COALESCE(m.chemistry, 0) as chemistry,
        COALESCE(m.english, 0) as english,
        COALESCE(a.attendance_percent, 0) as attendance_percent
    FROM students s
    LEFT JOIN marks m ON s.id = m.student_id
    LEFT JOIN attendance a ON s.id = a.student_id
    GROUP BY s.id
    """

    df = pd.read_sql_query(query, conn)

    # =========================
    # TESTIMONIAL TABLE CREATE
    # =========================
    conn.execute("""
    CREATE TABLE IF NOT EXISTS testimonials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    if df.empty:
        st.warning("❌ No data found in database")
        conn.close()
        return

    # =========================
    # CLEAN DATA
    # =========================
    df = df.drop_duplicates(subset=["id"]).reset_index(drop=True)

    for col in ["maths", "physics", "chemistry", "english", "attendance_percent"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df.rename(columns={"attendance_percent": "attendance"}, inplace=True)

    # =========================
    # CALCULATIONS
    # =========================
    df["Total"] = df[["maths", "physics", "chemistry", "english"]].sum(axis=1)
    df["Average"] = df["Total"] / 4

    results = df.apply(lambda row: predict_grade(row["Average"], row["attendance"]), axis=1)
    df["AI_Result"] = results.apply(lambda x: x[0])
    df["AI_Score"] = results.apply(lambda x: x[1])

    df["Improvement_Score"] = df["AI_Score"] - 50

    improved_count = (df["Improvement_Score"] > 10).sum()

    if improved_count > 0:
        st.success(f"🎉 {improved_count} Students Showing Improvement!")
        st.balloons()

    # =========================
    # SESSION
    # =========================
    role = st.session_state.get("role", "student")
    user = st.session_state.get("user", None)

    table_df = df.copy()

    if role == "student" and user:
        table_df = table_df[table_df["name"].str.lower() == user.lower()]



    # =========================
    # SIDEBAR
    # =========================

    # ROLE BASED SIDEBAR TITLE
    if role == "admin":
        st.sidebar.title("⚙ Admin Control Panel")

    elif role == "teacher":
        st.sidebar.title("👩‍🏫 Teacher Panel")

    else:
        st.sidebar.title("🎓 Student Panel")

    classes = ["All Classes"] + sorted(df["class"].dropna().unique().tolist())

    selected_class = st.sidebar.selectbox("📚 Select Class", classes)

    search = st.sidebar.text_input("🔍 Search Student")

    min_marks = st.sidebar.slider("📊 Min Average Marks", 0, 100, 0)

    min_attendance = st.sidebar.slider("📅 Min Attendance", 0, 100, 0)

    st.sidebar.info(f"👤 User: {user}")
    st.sidebar.info(f"🔐 Role: {role}")

    # ROLE ACCESS MESSAGE
    if role == "student":
        st.sidebar.warning("⚠ Limited Access Mode")

    elif role == "teacher":
        st.sidebar.success("✅ Teacher Access Enabled")

    else:
        st.sidebar.success("✅ Full Admin Access")

    # =========================
    # FILTERING
    # =========================
    filtered = table_df.copy()

    if selected_class != "All Classes":
        filtered = filtered[filtered["class"] == selected_class]

    if search:
        filtered = filtered[
            filtered["name"].str.lower().str.contains(search.lower(), na=False)
        ]

    filtered = filtered[
        (filtered["Average"] >= min_marks) &
        (filtered["attendance"] >= min_attendance)
    ]

    # =========================
    # KPI
    # =========================

    # ROLE BASED HEADING
    if role == "admin":
        st.markdown("## 📊 Admin Dashboard Overview")

    elif role == "teacher":
        st.markdown("## 👩‍🏫 Teacher Dashboard")

    else:
        st.markdown("## 🎓 Student Dashboard")


    
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👨‍🎓 Students", len(df))
    col2.metric("📈 Avg Marks", round(df["Average"].mean(), 2))
    col3.metric("🏆 Top Score", int(df["Total"].max()))
    col4.metric("⚠ Weak Students", len(df[df["AI_Score"] < 60]))

    st.markdown("---")

    # =========================
    # TABLE
    # =========================
    st.markdown("## 📚 Student Database")

    st.dataframe(filtered, use_container_width=True, height=350)

    st.markdown("---")

    # =========================
    # PROFILE VIEWER
    # =========================
    st.markdown("## 👤 Student Profile Viewer")

    if df["name"].nunique() > 0:

        student_name = st.selectbox("Select Student", df["name"].unique())

        profile = df[df["name"] == student_name]

        if not profile.empty:
            st.dataframe(profile)

            st.metric("Average", float(profile["Average"].iloc[0]))
            st.metric("Attendance", float(profile["attendance"].iloc[0]))
            st.metric("AI Score", float(profile["AI_Score"].iloc[0]))

    st.markdown("---")

    # =========================
    # TOP PERFORMERS
    # =========================
    st.markdown("## 🏆 Top Performers")

    top5 = df.sort_values("Average", ascending=False).head(5)

    st.dataframe(top5[["name", "class", "Average", "AI_Score"]])

    st.markdown("---")

    # =========================
    # WEAK STUDENTS
    # =========================
    st.markdown("## ⚠ Risk Analysis Panel")

    weak = df[df["AI_Score"] < 60]

    if weak.empty:
        st.success("🎉 No weak students detected 🚀")

    else:
        st.warning(f"🚨 {len(weak)} Students Found")

        st.dataframe(
            weak[["name", "class", "Average", "attendance", "AI_Score"]]
        )

    # =========================
    # NOTIFICATIONS
    # =========================
    if len(weak) > 0:
        notify_once(
            "weak_students",
            f"{len(weak)} weak students detected",
            "warning"
        )

    if df["attendance"].mean() < 75:
        notify_once(
            "low_attendance",
            "Class attendance is low",
            "error"
        )

    st.markdown("---")
    

    # =========================
    # LIVE NOTIFICATIONS
    # =========================
    st.markdown("## 📡 Live Notifications")

    notifications = get_notifications()

    if notifications:

        for n in reversed(notifications[-5:]):

            if n["level"] == "error":
                st.error(f"🚨 {n['message']} 🕒 {n['time']}")

            elif n["level"] == "warning":
                st.warning(f"⚠ {n['message']} 🕒 {n['time']}")

            else:
                st.info(f"ℹ {n['message']} 🕒 {n['time']}")

    else:
        st.success("No live notifications 🎉")

    st.markdown("---")


    # =========================
    # TESTIMONIAL PANEL
    # =========================
    st.markdown("## 💬 Student Testimonials")

    with st.form("testimonial_form"):

        testimonial_name = st.text_input("👤 Your Name")

        testimonial_message = st.text_area(
            "✍ Share your feedback or message for admin"
        )

        submit_testimonial = st.form_submit_button(
            "🚀 Submit Feedback"
        )

        if submit_testimonial:

            if testimonial_name and testimonial_message:

                conn.execute(
                    """
                    INSERT INTO testimonials
                    (student_name, message)
                    VALUES (?, ?)
                    """,
                    (testimonial_name, testimonial_message)
                )

                conn.commit()

                st.success("✅ Feedback Submitted Successfully!")

                notify_once(
                    f"testimonial_{testimonial_name}",
                    f"New testimonial from {testimonial_name}",
                    "info"
                )

            else:
                st.warning("⚠ Please fill all fields")

    st.markdown("### 🌟 Recent Student Feedback")

    testimonials = pd.read_sql_query(
        """
        SELECT student_name, message, created_at
        FROM testimonials
        ORDER BY id DESC
        LIMIT 5
        """,
        conn
    )

    if not testimonials.empty:

        for _, row in testimonials.iterrows():

            st.markdown(
                f"""
                <div style="
                    background:#1e1e1e;
                    padding:20px;
                    border-radius:15px;
                    margin-bottom:15px;
                    border-left:5px solid #00ff99;
                    box-shadow:0 2px 10px rgba(0,0,0,0.4);
                ">

                <h4 style="
                    color:white;
                    margin-bottom:10px;
                    font-size:20px;
                ">
                    👤 {row['student_name']}
                </h4>

                <p style="
                    color:#f1f1f1;
                    font-size:16px;
                    line-height:1.7;
                    margin-bottom:12px;
                ">
                    {row['message']}
                </p>

                <p style="
                    color:#bdbdbd;
                    font-size:12px;
                ">
                    🕒 {row['created_at']}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        st.info("No testimonials yet.")



    # =========================
    # AI INSIGHTS
    # =========================
    st.markdown("## 🧠 AI Insights")

    show_ai_insights(df)

    st.markdown("---")

    # =========================
    # CHARTS
    # =========================
    st.subheader("📊 Analytics Dashboard")

    show_bar_chart(df)

    st.markdown("---")

    show_attendance_chart(df)

    st.markdown("---")

    show_pie_chart(df)

    st.markdown("---")

    # =========================
    # CHATBOT
    # =========================
    st.subheader("🤖 AI Student Assistant")

    try:
        chatbot(df)

    except:
        st.warning("Chatbot temporarily unavailable")

    st.markdown("---")

    # =========================
    # PDF EXPORT
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

        for _, row in data.iterrows():

            text = (
                f"{row['name']} | "
                f"{row['class']} | "
                f"{row['Average']:.2f} | "
                f"{row['attendance']}% | "
                f"{row['AI_Result']}"
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
        "📥 Download PDF Report",
        pdf_file,
        "student_report.pdf",
        "application/pdf"
    )

    # =========================
    # CSV EXPORT
    # =========================
    @st.cache_data
    def convert_excel(data):
        return data.to_csv(index=False).encode("utf-8")

    csv = convert_excel(df)

    st.download_button(
        "📥 Download Excel Report",
        csv,
        "students.csv",
        "text/csv"
    )

    st.markdown("---")

    st.caption("🚀 Built with Streamlit | AI Student Intelligence System")

    conn.close()
