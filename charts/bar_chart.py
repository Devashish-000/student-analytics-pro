import streamlit as st
import plotly.graph_objects as go


def show_bar_chart(df):

    st.subheader("📊 Premium 3D Performance Chart")

    # =========================
    # SAFETY CHECK
    # =========================
    if "name" not in df.columns or "Total" not in df.columns:

        st.error(
            "Required columns missing: name / Total"
        )

        return

    # =========================
    # CLEAN DATA
    # =========================
    chart_df = df[
        ["name", "Total"]
    ].dropna()

    chart_df = chart_df.sort_values(
        by="Total",
        ascending=False
    )

    # =========================
    # CREATE 3D EFFECT BARS
    # =========================
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=chart_df["name"],
            y=chart_df["Total"],

            text=chart_df["Total"],

            textposition='outside',

            hovertemplate=
            "<b>Student:</b> %{x}<br>" +
            "<b>Total Marks:</b> %{y}<br>" +
            "<extra></extra>"
        )
    )

    # =========================
    # PREMIUM LAYOUT
    # =========================
    fig.update_layout(

        title={
            "text": "🚀 Student Performance Analytics",
            "x": 0.5
        },

        xaxis_title="Students",

        yaxis_title="Total Marks",

        template="plotly_dark",

        height=600,

        hovermode="x unified",

        paper_bgcolor="#0f172a",

        plot_bgcolor="#111827",

        font=dict(
            size=14
        ),

        margin=dict(
            l=40,
            r=40,
            t=80,
            b=40
        )
    )

    # =========================
    # BAR STYLE
    # =========================
    fig.update_traces(

        marker=dict(
            line=dict(
                width=1
            )
        )
    )

    # =========================
    # SHOW CHART
    # =========================
    st.plotly_chart(
        fig,
        use_container_width=True
    )
