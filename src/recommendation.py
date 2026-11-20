import streamlit as st
import pandas as pd
import plotly.express as px
from src.utils import load_data

st.set_page_config(
    page_title="Music Recommendation",
    page_icon="🎵",
    layout="wide"
)

st.title("🎵 Smart Music Recommendation")
st.caption("Discover songs from your favorite artists")

# ===============================
# LOAD DATA
# ===============================

try:
    df = load_data()

    if df is None or df.empty:
        st.error("Dataset is empty.")
        st.stop()

except Exception as e:
    st.error(f"Error loading dataset:\n{e}")
    st.stop()

# ===============================
# REQUIRED COLUMNS CHECK
# ===============================

required = [
    "artist",
    "song",
    "popularity"
]

missing = [
    c for c in required
    if c not in df.columns
]

if missing:
    st.error(
        f"Missing columns: {missing}"
    )
    st.write(df.columns.tolist())
    st.stop()

df = df.drop_duplicates(
    subset=["artist", "song"]
)

# ===============================
# SELECT BOXES
# ===============================

artists = sorted(
    df["artist"].dropna().unique()
)

artist = st.selectbox(
    "Select Artist",
    artists
)

songs = sorted(
    df[
        df["artist"] == artist
    ]["song"].dropna().unique()
)

song = st.selectbox(
    "Select Song",
    songs
)

# ===============================
# SONG INFO
# ===============================

selected = df[
    (df["artist"] == artist)
    &
    (df["song"] == song)
]

if selected.empty:
    st.warning("Song not found.")
    st.stop()

selected = selected.iloc[0]

st.divider()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Popularity",
        selected.get(
            "popularity",
            "N/A"
        )
    )

with c2:
    st.metric(
        "Album",
        selected.get(
            "album_type",
            "N/A"
        )
    )

with c3:
    duration = selected.get(
        "duration_minutes",
        None
    )

    if duration is not None:
        st.metric(
            "Duration",
            f"{duration:.2f} min"
        )

# ===============================
# RECOMMENDATIONS
# ===============================

if st.button(
    "🎯 Generate Recommendations"
):

    recommendations = df[
        (df["artist"] == artist)
        &
        (df["song"] != song)
    ].copy()

    recommendations = recommendations.sort_values(
        by="popularity",
        ascending=False
    )

    if recommendations.empty:

        st.warning(
            "This artist has only one song in dataset."
        )

        recommendations = df[
            df["song"] != song
        ].sort_values(
            by="popularity",
            ascending=False
        ).head(10)

    st.success(
        f"{len(recommendations)} songs found"
    )

    st.subheader(
        "🎵 Recommendations"
    )

    st.dataframe(
        recommendations[
            [
                "song",
                "artist",
                "popularity"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    fig = px.bar(
        recommendations.head(10),
        x="popularity",
        y="song",
        color="artist",
        orientation="h"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )