import streamlit as st
import pandas as pd

from src.utils import load_data
from src.charts import (
    top_artists_chart,
    top_songs_chart,
    album_distribution_chart,
    popularity_distribution,
    monthly_trend,
    yearly_trend,
    compare_artists,
    correlation_heatmap,
)

# ----------------------------------------------------
# Page Config
# ----------------------------------------------------

st.set_page_config(
    page_title="Analytics | K-Wave Analytics",
    page_icon="📊",
    layout="wide"
)

# ----------------------------------------------------
# Custom CSS
# ----------------------------------------------------

st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

.block-container{
    padding-top:1.5rem;
}

.metric-card{
    background:#1E1E1E;
    border-radius:15px;
    padding:20px;
    text-align:center;
    border:1px solid #343541;
}

.metric-title{
    color:#AAAAAA;
    font-size:16px;
}

.metric-value{
    color:white;
    font-size:34px;
    font-weight:bold;
}

.chart-card{
    background:#1E1E1E;
    padding:20px;
    border-radius:15px;
}

h1,h2,h3{
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# Load Dataset
# ----------------------------------------------------

df = load_data()

# ----------------------------------------------------
# Header
# ----------------------------------------------------

st.title("📊 K-Wave Analytics")

st.caption(
    "AI Powered K-Pop Trend Intelligence Platform"
)


# ----------------------------------------------------
# Sidebar Filters
# ----------------------------------------------------

st.sidebar.title("🎛 Analytics Filters")

artists = sorted(
    df["artist"].unique()
)

albums = sorted(
    df["album_type"].unique()
)

years = sorted(
    df["release_year"].unique()
)

months = sorted(
    df["release_month"].unique()
)

selected_artists = st.sidebar.multiselect(
    "Artist",
    artists
)

selected_album = st.sidebar.multiselect(
    "Album Type",
    albums
)

selected_year = st.sidebar.multiselect(
    "Release Year",
    years
)

selected_month = st.sidebar.multiselect(
    "Release Month",
    months
)

# ----------------------------------------------------
# Apply Filters
# ----------------------------------------------------

filtered = df.copy()

if selected_artists:

    filtered = filtered[
        filtered["artist"].isin(
            selected_artists
        )
    ]

if selected_album:

    filtered = filtered[
        filtered["album_type"].isin(
            selected_album
        )
    ]

if selected_year:

    filtered = filtered[
        filtered["release_year"].isin(
            selected_year
        )
    ]

if selected_month:

    filtered = filtered[
        filtered["release_month"].isin(
            selected_month
        )
    ]

# ----------------------------------------------------
# Analysis Data
# Search Removed
# ----------------------------------------------------

result = filtered

st.divider()

# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------

songs = len(filtered)

artists_count = filtered["artist"].nunique()

if len(filtered) > 0:

    avg_popularity = round(
        filtered["popularity"].mean(),
        2
    )

else:

    avg_popularity = 0

trending = len(
    filtered[
        filtered["trending_label"] == 1
    ]
)

c1, c2, c3, c4 = st.columns(4)

# ----------------------------------------------------
# Total Songs
# ----------------------------------------------------

with c1:

    st.markdown(
        f"""
        <div class="metric-card">

        <div class="metric-title">
        🎵 Total Songs
        </div>

        <div class="metric-value">
        {songs}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------------------------------------
# Artists
# ----------------------------------------------------

with c2:

    st.markdown(
        f"""
        <div class="metric-card">

        <div class="metric-title">
        👨‍🎤 Artists
        </div>

        <div class="metric-value">
        {artists_count}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------------------------------------
# Average Popularity
# ----------------------------------------------------

with c3:

    st.markdown(
        f"""
        <div class="metric-card">

        <div class="metric-title">
        ⭐ Avg Popularity
        </div>

        <div class="metric-value">
        {avg_popularity}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------------------------------------
# Trending Songs
# ----------------------------------------------------

with c4:

    st.markdown(
        f"""
        <div class="metric-card">

        <div class="metric-title">
        🔥 Trending Songs
        </div>

        <div class="metric-value">
        {trending}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# ----------------------------------------------------
# Tabs
# ----------------------------------------------------

tab1, tab2, tab3 = st.tabs(
    [
        "👨‍🎤 Artist Analytics",
        "🎵 Song Analytics",
        "📈 Trend Analysis"
    ]
)

# ==========================================================
# TAB 1 : ARTIST ANALYTICS
# ==========================================================

with tab1:

    st.subheader(
        "👨‍🎤 Artist Analytics"
    )

    if result.empty:

        st.warning(
            "No data available for the selected filters."
        )

    else:

        col1, col2 = st.columns(2)

        # --------------------------------------------------
        # Top Artists
        # --------------------------------------------------

        with col1:

            st.plotly_chart(
                top_artists_chart(result),
                use_container_width=True
            )

        # --------------------------------------------------
        # Album Distribution
        # --------------------------------------------------

        with col2:

            st.plotly_chart(
                album_distribution_chart(result),
                use_container_width=True
            )

        st.write("")

        # --------------------------------------------------
        # Artist Statistics
        # --------------------------------------------------

        st.subheader(
            "Artist Statistics"
        )

        artist_stats = (

            result

            .groupby("artist")

            .agg(
                Songs=("song", "count"),

                Average_Popularity=(
                    "popularity",
                    "mean"
                ),

                Highest_Popularity=(
                    "popularity",
                    "max"
                ),

                Avg_Duration=(
                    "duration_minutes",
                    "mean"
                )
            )

            .reset_index()
        )

        artist_stats[
            "Average_Popularity"
        ] = (

            artist_stats[
                "Average_Popularity"
            ]

            .round(2)
        )

        artist_stats[
            "Avg_Duration"
        ] = (

            artist_stats[
                "Avg_Duration"
            ]

            .round(2)
        )

        st.dataframe(
            artist_stats,
            use_container_width=True,
            height=400
        )


# ==========================================================
# TAB 2 : SONG ANALYTICS
# ==========================================================

with tab2:

    st.subheader(
        "🎵 Song Analytics"
    )

    if result.empty:

        st.warning(
            "No data available for the selected filters."
        )

    else:

        left, right = st.columns(2)

        # --------------------------------------------------
        # Top Songs Chart
        # --------------------------------------------------

        with left:

            st.plotly_chart(
                top_songs_chart(result),
                use_container_width=True
            )

        # --------------------------------------------------
        # Popularity Distribution
        # --------------------------------------------------

        with right:

            st.plotly_chart(
                popularity_distribution(result),
                use_container_width=True
            )

        st.write("")

        # --------------------------------------------------
        # Top Songs Table
        # --------------------------------------------------

        st.subheader(
            "Top Songs"
        )

        top_songs = (

            result

            .sort_values(
                "popularity",
                ascending=False
            )

            [
                [
                    "song",
                    "artist",
                    "popularity",
                    "position",
                    "album_type"
                ]
            ]
        )

        st.dataframe(
            top_songs,
            use_container_width=True,
            height=450
        )

        st.write("")

        # --------------------------------------------------
        # Song Selection
        # --------------------------------------------------

        st.subheader(
            "Song Details"
        )

        selected_song = st.selectbox(
            "Choose Song",
            sorted(
                result["song"].unique()
            )
        )

        if selected_song:

            song = result[
                result["song"] == selected_song
            ].iloc[0]

            c1, c2 = st.columns([1, 2])

            # ------------------------------------------------
            # Album Cover
            # ------------------------------------------------

            with c1:

                if (
                    isinstance(
                        song["album_cover_url"],
                        str
                    )
                    and
                    song["album_cover_url"].startswith(
                        "http"
                    )
                ):

                    st.image(
                        song["album_cover_url"],
                        width=250
                    )

            # ------------------------------------------------
            # Song Information
            # ------------------------------------------------

            with c2:

                st.metric(
                    "Artist",
                    song["artist"]
                )

                st.metric(
                    "Popularity",
                    song["popularity"]
                )

                st.metric(
                    "Rank",
                    song["position"]
                )

                st.metric(
                    "Album",
                    song["album_type"]
                )

                st.metric(
                    "Duration",
                    f"{song['duration_minutes']} min"
                )

                st.metric(
                    "Tracks",
                    song["total_tracks"]
                )


# ==========================================================
# TAB 3 : TREND ANALYSIS
# ==========================================================

with tab3:

    st.subheader(
        "📈 Trend Analysis"
    )

    if result.empty:

        st.warning(
            "No data available for the selected filters."
        )

    else:

        col1, col2 = st.columns(2)

        # --------------------------------------------------
        # Monthly Trend
        # --------------------------------------------------

        with col1:

            st.plotly_chart(
                monthly_trend(result),
                use_container_width=True
            )

        # --------------------------------------------------
        # Yearly Trend
        # --------------------------------------------------

        with col2:

            st.plotly_chart(
                yearly_trend(result),
                use_container_width=True
            )

        st.write("")

        # --------------------------------------------------
        # Correlation Heatmap
        # --------------------------------------------------

        st.plotly_chart(
            correlation_heatmap(result),
            use_container_width=True
        )

        st.write("")

        # --------------------------------------------------
        # Trending Songs
        # --------------------------------------------------

        st.subheader(
            "🔥 Trending Songs"
        )

        trending_df = result[
            result["trending_label"] == 1
        ]

        if trending_df.empty:

            st.info(
                "No trending songs found for the selected filters."
            )

        else:

            st.dataframe(
                trending_df[
                    [
                        "song",
                        "artist",
                        "popularity",
                        "position",
                        "release_year"
                    ]
                ],
                use_container_width=True,
                height=400
            )


# ==========================================================
# DOWNLOAD SECTION
# ==========================================================

st.divider()

st.subheader(
    "📥 Download Filtered Dataset"
)

csv = result.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇ Download CSV",
    data=csv,
    file_name="filtered_kwave_dataset.csv",
    mime="text/csv"
)

st.divider()

# ----------------------------------------------------
# Footer
# ----------------------------------------------------

st.caption(
    "© 2026 K-Wave Analytics | "
    "AI-Powered K-Pop Trend Intelligence Platform"
)