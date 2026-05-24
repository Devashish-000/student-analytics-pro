import streamlit as st
import plotly.graph_objects as go


def show_pie_chart(df):

    st.subheader("🥧 Premium Pass vs Fail Analytics")

    if df.empty:
        st.warning("No data available")
        return

    if "Average" not in df.columns:
        st.error("Average column missing")
        return

    df = df.dropna(subset=["Average"])

    pass_count = (df["Average"] >= 60).sum()
    fail_count = (df["Average"] < 60).sum()

    fig = go.Figure(
        data=[
            go.Pie(
                labels=["Pass", "Fail"],
                values=[pass_count, fail_count],
                hole=0.5,
                textinfo="label+percent",
                marker=dict(colors=["#22c55e", "#ef4444"])
            )
        ]
    )

    fig.update_layout(
        title="🚀 Student Result Distribution",
        paper_bgcolor="#0f172a",
        plot_bgcolor="#111827",
        font=dict(color="white"),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)
