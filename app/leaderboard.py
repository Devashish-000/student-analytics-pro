import streamlit as st

def show_leaderboard(df):

    st.subheader("🏆 Student Leaderboard")

    # Sort by total marks
    df = df.sort_values(by="Total", ascending=False).reset_index(drop=True)

    # Rank column
    df["Rank"] = df.index + 1

    # Badge system
    def get_badge(rank):
        if rank == 1:
            return "🥇 Gold"
        elif rank == 2:
            return "🥈 Silver"
        elif rank == 3:
            return "🥉 Bronze"
        else:
            return "⭐"

    df["Badge"] = df["Rank"].apply(get_badge)

    # Show top columns only
    leaderboard_df = df[["Rank", "name", "class", "Total", "Average", "Badge"]]

    st.dataframe(leaderboard_df, use_container_width=True)

    # Highlight top 3
    st.success("🏆 Top Performers Updated Live!")
