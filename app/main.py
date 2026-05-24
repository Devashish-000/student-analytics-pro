import streamlit as st
from datetime import datetime

# =========================
# APP MODULE IMPORTS (FIXED FOR STREAMLIT CLOUD)
# =========================
from app.login import login_page
from app.dashboard import show_dashboard
from app.crud import crud_page
from app.profile import profile_page
from app.ranking import ranking_page

from app.notice import notice_page
from app.fees import fees_page
from app.alerts import alerts_page


# =========================
# PAGE CONFIG (ONLY ONCE)
# =========================
st.set_page_config(
    page_title="Student Analytics Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================
# SESSION STATE INIT
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "role" not in st.session_state:
    st.session_state.role = None

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True


# =========================
# THEME SYSTEM
# =========================
def apply_theme():

    if st.session_state.dark_mode:
        st.markdown("""
        <style>
        .stApp {
            background: radial-gradient(circle at top, #0f172a, #020617);
            color: white;
        }

        section[data-testid="stSidebar"] {
            background: #0B1220;
        }

        div[data-testid="metric-container"] {
            background: rgba(255,255,255,0.06);
            border-radius: 15px;
            padding: 15px;
            border: 1px solid rgba(255,255,255,0.1);
        }

        .stButton > button {
            background: linear-gradient(90deg,#6366f1,#8b5cf6);
            color: white;
            border-radius: 10px;
            border: none;
        }

        h1,h2,h3,h4,h5,h6,p,span,label {
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <style>
        .stApp {
            background: #f8fafc;
            color: #111827;
        }

        section[data-testid="stSidebar"] {
            background: white;
        }

        div[data-testid="metric-container"] {
            background: white;
            border-radius: 15px;
            padding: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }

        .stButton > button {
            background: linear-gradient(90deg,#3b82f6,#06b6d4);
            color: white;
            border-radius: 10px;
            border: none;
        }
        </style>
        """, unsafe_allow_html=True)


# =========================
# HEADER
# =========================
def header():

    time = datetime.now().strftime("%d %b %Y | %I:%M %p")

    st.markdown(f"""
    <div style="
        padding:20px;
        border-radius:15px;
        text-align:center;
        background: rgba(255,255,255,0.05);
        margin-bottom:15px;
    ">
        <h1>🎓 Student Analytics Pro</h1>
        <p>🚀 AI Powered Dashboard</p>
        <small>🕒 {time}</small>
    </div>
    """, unsafe_allow_html=True)


# =========================
# MENU
# =========================
def menu():

    role = st.session_state.get("role")

    if role == "admin":
        return [
            "Dashboard",
            "CRUD",
            "Notice Board",
            "Fees Panel",
            "Alerts",
            "Profile",
            "Ranking"
        ]

    return [
        "Dashboard",
        "Notice Board",
        "Fees Panel",
        "Alerts",
        "Profile",
        "Ranking"
    ]


# =========================
# MAIN APP
# =========================
def main():

    apply_theme()

    # LOGIN SCREEN
    if not st.session_state.logged_in:
        login_page()
        return

    # SIDEBAR
    st.sidebar.title("⚡ PRO DASHBOARD")

    dark = st.sidebar.checkbox(
        "🌙 Dark Mode",
        value=st.session_state.dark_mode
    )

    st.session_state.dark_mode = dark

    st.sidebar.markdown("---")

    page = st.sidebar.selectbox(
        "🧭 Navigation",
        menu()
    )

    st.sidebar.markdown("---")

    st.sidebar.success(f"👤 {st.session_state.user}")
    st.sidebar.info(f"🔐 {st.session_state.role}")

    # LOGOUT
    if st.sidebar.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None

        st.rerun()   # ✅ FIXED (NEW STREAMLIT WAY)

    header()

    # =========================
    # ROUTING
    # =========================
    if page == "Dashboard":
        show_dashboard()

    elif page == "CRUD":
        crud_page()

    elif page == "Notice Board":
        notice_page()

    elif page == "Fees Panel":
        fees_page()

    elif page == "Alerts":
        alerts_page()

    elif page == "Profile":
        profile_page()

    elif page == "Ranking":
        ranking_page()


if __name__ == "__main__":
    main()
