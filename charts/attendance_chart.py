import streamlit as st
import plotly.graph_objects as go


def show_attendance_chart(df):

    st.subheader("📈 Premium Attendance Analytics")

    # =========================
    # FIXED COLUMN NAME
    # =========================
    if "attendance" not in df.columns or "name" not in df.columns:
        st.error("Attendance column missing")
        return

    chart_df = df[["name", "attendance"]].dropna()

    if chart_df.empty:
        st.warning("No attendance data available")
        return

    chart_df = chart_df.sort_values(by="attendance", ascending=False)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=chart_df["name"],
            y=chart_df["attendance"],

            mode="lines+markers+text",
            text=[f"{v}%" for v in chart_df["attendance"]],
            textposition="top center",

            line=dict(color="#00E5FF", width=4, shape="spline"),

            marker=dict(
                size=12,
                color=chart_df["attendance"],
                colorscale="Turbo",
                line=dict(color="white", width=1)
            ),

            hovertemplate="<b>%{x}</b><br>Attendance: %{y}%<extra></extra>"
        )
    )

    fig.update_layout(
        title="📈 Attendance Performance",
        paper_bgcolor="#0f172a",
        plot_bgcolor="#111827",
        font=dict(color="white"),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)
