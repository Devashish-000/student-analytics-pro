import streamlit as st

def show_ai_insights(df):

    st.subheader("🧠 AI Insights Engine")

    if df.empty:
        st.warning("No data available")
        return

    insights = []

    # Top performer
    if "Average" in df.columns:
        top = df.loc[df["Average"].idxmax()]
        insights.append(f"🏆 Top Performer: {top['name']}")

    # Weak students
    if "Average" in df.columns:
        weak = df[df["Average"] < 40]
        insights.append(f"⚠ Weak Students: {len(weak)}")

    # Attendance risk
    if "attendance_percent" in df.columns:
        low_att = df[df["attendance_percent"] < 75]
        insights.append(f"📉 Low Attendance Students: {len(low_att)}")

    for i in insights:
        st.info(i)
