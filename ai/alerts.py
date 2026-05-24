import streamlit as st

def smart_alerts(df):

    st.subheader("🔔 Smart Alerts System")

    if "attendance_percent" in df.columns:

        low = df[df["attendance_percent"] < 75]

        if len(low) > 0:
            st.error(f"🚨 {len(low)} students have low attendance!")
        else:
            st.success("All students have good attendance 🚀")

    if "Average" in df.columns:

        weak = df[df["Average"] < 40]

        if len(weak) > 0:
            st.warning(f"⚠ {len(weak)} weak students detected")
