import streamlit as st
import pandas as pd
import plotly.express as px

from src.utils import load_data


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Music Recommendation",
    page_icon="🎵",
    layout="wide"
)


# ==========================================================
# HEADER
# ==========================================================

st.title("🎵 Smart Music Recommendation")

st.caption(
    "Discover other songs from your favourite artists"
)


# ==========================================================
# LOAD DATA
# ==========================================================

try:

    df = load_data()

except Exception as e:

    st.error(e)

    st.stop()


# ==========================================================
# CHECK REQUIRED COLUMNS
# ==========================================================

required = [
    "artist",
    "song",
    "popularity"
]

missing = [
    c
    for c in required
    if c not in df.columns
]

if missing:

    st.error(
        f"Missing columns : {missing}"
    )

    st.write(
        df.columns.tolist()
    )

    st.stop()


# ==========================================================
# REMOVE DUPLICATE SONGS
# ==========================================================

df = df.drop_duplicates(
    subset=["artist", "song"]
)


# ==========================================================
# ARTIST
# ==========================================================

artists = sorted(
    df["artist"]
    .dropna()
    .unique()
)

artist = st.selectbox(
    "Select Artist",
    artists
)


# ==========================================================
# SONGS
# ==========================================================

songs = sorted(
    df[
        df["artist"] == artist
    ]["song"]
    .dropna()
    .unique()
)

song = st.selectbox(
    "Select Song",
    songs
)


# ==========================================================
# SELECTED SONG
# ==========================================================

selected = df[
    (df["artist"] == artist)
    &
    (df["song"] == song)
].iloc[0]


# ==========================================================
# SONG INFORMATION
# ==========================================================

st.divider()

c1, c2, c3 = st.columns(3)


# ----------------------------------------------------------
# POPULARITY
# ----------------------------------------------------------

with c1:

    st.metric(
        "Popularity",
        selected.get(
            "popularity",
            0
        )
    )


# ----------------------------------------------------------
# ALBUM TYPE
# ----------------------------------------------------------

with c2:

    st.metric(
        "Album Type",
        selected.get(
            "album_type",
            "Unknown"
        )
    )


# ----------------------------------------------------------
# DURATION
# ----------------------------------------------------------

with c3:

    duration = selected.get(
        "duration_minutes",
        0
    )

    st.metric(
        "Duration",
        f"{duration:.2f} min"
    )


# ==========================================================
# RECOMMEND BUTTON
# ==========================================================

if st.button(
    "🎯 Generate Recommendations",
    use_container_width=True
):

    # ======================================================
    # FIND OTHER SONGS FROM SAME ARTIST
    # ======================================================

    recommendations = df[
        (df["artist"] == artist)
        &
        (df["song"] != song)
    ].copy()


    # ======================================================
    # SORT BY POPULARITY
    # ======================================================

    recommendations = recommendations.sort_values(
        by="popularity",
        ascending=False
    )


    # ======================================================
    # IF ARTIST HAS NO OTHER SONG
    # USE OTHER SONGS FROM DATASET
    # ======================================================

    if recommendations.empty:

        recommendations = df[
            df["song"] != song
        ].sort_values(
            by="popularity",
            ascending=False
        )


    # ======================================================
    # LIMIT TO TOP 10
    # ======================================================

    recommendations = recommendations.head(10)


    # ======================================================
    # RECOMMENDED SONGS
    # ======================================================

    st.subheader(
        "🎵 Recommended Songs"
    )


    # ======================================================
    # RECOMMENDATION TABLE
    # ======================================================

    table = recommendations[
        [
            "song",
            "artist",
            "popularity"
        ]
    ]


    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )


    # ======================================================
    # POPULARITY CHART
    # ======================================================

    fig = px.bar(
        recommendations,
        x="popularity",
        y="song",
        color="artist",
        orientation="h",
        text="popularity"
    )


    fig.update_layout(
        height=600
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ======================================================
    # TOP RECOMMENDATION
    # ======================================================

    best = recommendations.iloc[0]


    st.subheader(
        "🥇 Top Recommendation"
    )


    st.success(
        f"{best['song']} by {best['artist']}"
    )