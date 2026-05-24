import streamlit as st

def chatbot(df):

    st.subheader("🤖 AI Smart Chatbot (v2)")

    if df is None or df.empty:
        st.warning("No data available for chatbot")
        return

    user_input = st.text_input("💬 Ask about students:")

    if not user_input:
        return

    query = user_input.lower()

    # =========================
    # TOP STUDENT
    # =========================
    if "top" in query:
        top = df.loc[df["Average"].idxmax()]
        st.success(f"🏆 Top Student: {top['name']} | Avg: {top['Average']:.2f}")

    # =========================
    # WEAK STUDENTS
    # =========================
    elif "weak" in query:
        weak = df[df["Average"] < 60]
        st.warning(f"⚠ Weak Students: {len(weak)}")

        st.dataframe(weak[["name", "Average"]])

    # =========================
    # ATTENDANCE QUERY
    # =========================
    elif "attendance" in query:
        name_found = False

        for _, row in df.iterrows():
            if row["name"].lower() in query:
                st.info(f"📊 {row['name']} Attendance: {row['attendance']}%")
                name_found = True
                break

        if not name_found:
            st.info(f"📊 Avg Attendance: {df['attendance'].mean():.2f}%")

    # =========================
    # MARKS QUERY
    # =========================
    elif "marks" in query:
        if "maths" in query:
            st.info(f"📘 Avg Maths: {df['maths'].mean():.2f}")
        elif "physics" in query:
            st.info(f"📗 Avg Physics: {df['physics'].mean():.2f}")
        elif "chemistry" in query:
            st.info(f"📙 Avg Chemistry: {df['chemistry'].mean():.2f}")
        elif "english" in query:
            st.info(f"📕 Avg English: {df['english'].mean():.2f}")
        else:
            st.info(f"📊 Overall Avg Marks: {df['Average'].mean():.2f}")

    # =========================
    # STUDENT SEARCH
    # =========================
    elif any(name.lower() in query for name in df["name"]):

        for _, row in df.iterrows():
            if row["name"].lower() in query:
                st.success(f"""
                👤 {row['name']}
                📊 Avg: {row['Average']}
                🎯 AI Score: {row['AI_Score']}
                🏅 Grade: {row['AI_Result']}
                """)

    # =========================
    # FALLBACK (SMART REPLY)
    # =========================
    else:
        st.info("🤖 I can help with: top student, weak students, marks, attendance, student details")
