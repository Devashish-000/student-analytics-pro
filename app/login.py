import streamlit as st
import sqlite3
import os

from app.utils.security import verify_password

# =========================
# DB CONNECTION
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "../database/school.db")

conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()


# =========================
# LOGIN PAGE
# =========================
def login_page():

    # =========================
    # PAGE STYLE
    # =========================
    st.markdown(
        """
        <style>

        .main {
            background-color: #0f172a;
        }

        .login-box {
            max-width: 420px;
            margin: auto;
            margin-top: 90px;
            padding: 35px;
            border-radius: 15px;
            background: #111827;
            box-shadow: 0 0 25px rgba(0,0,0,0.5);
        }

        .title {
            text-align: center;
            font-size: 30px;
            font-weight: bold;
            color: white;
            margin-bottom: 10px;
        }

        .subtitle {
            text-align: center;
            font-size: 13px;
            color: #9ca3af;
            margin-bottom: 25px;
        }

        .stTextInput > div > div > input {
            background-color: #1f2937;
            color: white;
            border-radius: 8px;
        }

        .stButton > button {
            width: 100%;
            background: linear-gradient(90deg, #6366f1, #22c55e);
            color: white;
            border-radius: 8px;
            height: 45px;
            font-weight: bold;
            border: none;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # LOGIN UI
    # =========================
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    st.markdown(
        "<div class='title'>🎓 Student Analytics</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>AI Powered Performance System Login</div>",
        unsafe_allow_html=True
    )

    username = st.text_input("👤 Username")

    password = st.text_input("🔑 Password", type="password")

    # =========================
    # LOGIN BUTTON
    # =========================
    if st.button("Login 🚀"):

        if not username or not password:
            st.warning("Please enter username and password ❗")
            return

        # =========================
        # ADMIN / STUDENT LOGIN
        # =========================
        cursor.execute(
            "SELECT username, password, role FROM users WHERE username=?",
            (username,)
        )

        user = cursor.fetchone()

        # =========================
        # VERIFY ADMIN/STUDENT
        # =========================
        if user:

            db_username, db_password, db_role = user

            if verify_password(password, db_password):

                st.session_state.logged_in = True
                st.session_state.user = db_username
                st.session_state.role = db_role

                st.success(f"Welcome {db_username} 🚀 ({db_role})")

                try:
                    st.rerun()
                except:
                    st.experimental_rerun()

            else:
                st.error("❌ Invalid Password")

        # =========================
        # TEACHER LOGIN
        # =========================
        else:

            cursor.execute(
                "SELECT username, password FROM teachers WHERE username=?",
                (username,)
            )

            teacher = cursor.fetchone()

            if teacher:

                teacher_username, teacher_password = teacher

                if password == teacher_password:

                    st.session_state.logged_in = True
                    st.session_state.user = teacher_username
                    st.session_state.role = "teacher"

                    st.success(f"Welcome {teacher_username} 🚀 (teacher)")

                    try:
                        st.rerun()
                    except:
                        st.experimental_rerun()

                else:
                    st.error("❌ Invalid Teacher Password")

            else:
                st.error("❌ User Not Found")

    st.markdown("</div>", unsafe_allow_html=True)

