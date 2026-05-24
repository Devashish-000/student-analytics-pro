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
            max-width: 400px;
            margin: auto;
            margin-top: 100px;
            padding: 35px;
            border-radius: 15px;
            background: #111827;
            box-shadow: 0 0 25px rgba(0,0,0,0.5);
        }

        .title {
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            color: white;
            margin-bottom: 20px;
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
        "<div class='title'>🎓 Student Login</div>",
        unsafe_allow_html=True
    )

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    # =========================
    # LOGIN BUTTON
    # =========================
    if st.button("Login 🚀"):

        if username.strip() == "" or password.strip() == "":
            st.warning("Please enter username and password ❗")
            return

        # FETCH USER
        cursor.execute(
            "SELECT username, password, role FROM users WHERE username=?",
            (username,)
        )

        user = cursor.fetchone()

        # =========================
        # VERIFY USER
        # =========================
        if user:

            db_username = user[0]
            db_password = user[1]
            db_role = user[2]

            # VERIFY HASHED PASSWORD
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
                st.error("Invalid Password ❌")

        else:
            st.error("User Not Found ❌")

    st.markdown("</div>", unsafe_allow_html=True)
