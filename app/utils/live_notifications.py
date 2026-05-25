import streamlit as st
from datetime import datetime


def init_notifications():
    if "notifications" not in st.session_state:
        st.session_state.notifications = []


def push_notification(message, level="info"):
    init_notifications()

    st.session_state.notifications.append({
        "message": message,
        "level": level,
        "time": datetime.now().strftime("%H:%M:%S")
    })


def get_notifications():
    init_notifications()
    return st.session_state.notifications


def clear_notifications():
    st.session_state.notifications = []
