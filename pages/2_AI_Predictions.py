import streamlit as st
import pandas as pd

from src.utils import load_data
from src.predict import predict_all


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AI Predictions",
    page_icon="🤖",
    layout="wide"
)


# ==========================================================
# LOAD DATA
# ==========================================================

df = load_data()


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

.main {
    background: #0E1117;
}

.block-container {
    padding-top: 1rem;
}

.result-card {
    background: #1E1E1E;
    border-radius: 18px;
    padding: 20px;
    border: 1px solid #333333;
    text-align: center;
}

.metric-title {
    color: #BBBBBB;
    font-size: 15px;
}

.metric-value {
    color: white;
    font-size: 34px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# HEADER
# ==========================================================

st.title("🤖 AI Prediction Center")

st.caption(
    "Predict Popularity • Trending • Top10 • Artist Success"
)

st.divider()


# ==========================================================
# EXISTING SONG SELECTION
# ==========================================================

st.subheader("🎵 Select an Existing Song")

col1, col2 = st.columns(2)


# ==========================================================
# ARTIST
# ==========================================================

with col1:

    artist = st.selectbox(
        "Artist",
        sorted(
            df["artist"]
            .dropna()
            .unique()
        ),
        key="artist_existing"
    )


# ==========================================================
# SONG
# ==========================================================

with col2:

    songs = sorted(
        df[
            df["artist"] == artist
        ]["song"]
        .dropna()
        .unique()
    )

    song = st.selectbox(
        "Song",
        songs,
        key="song_existing"
    )


# ==========================================================
# SELECTED SONG
# ==========================================================

selected = df[
    (df["artist"] == artist) &
    (df["song"] == song)
].iloc[0]


# ==========================================================
# ALBUM COVER ONLY
# ==========================================================

image_url = selected["album_cover_url"]

if (
    isinstance(image_url, str)
    and image_url.startswith("http")
):

    st.image(
        image_url,
        width=260
    )

else:

    st.info(
        "🎵 Album cover not available"
    )


# ==========================================================
# GET MODEL INPUTS
# ==========================================================

album_type = selected["album_type"]

duration = int(
    selected["duration_ms"]
)

tracks = int(
    selected["total_tracks"]
)

explicit = bool(
    selected["is_explicit"]
)

year = int(
    selected["release_year"]
)

month = int(
    selected["release_month"]
)


# ==========================================================
# DIVIDER
# ==========================================================

st.divider()


# ==========================================================
# PREDICT BUTTON
# ==========================================================

predict = st.button(
    "🚀 Predict Song Performance",
    key="predict_song",
    use_container_width=True
)


# ==========================================================
# PREDICTION
# ==========================================================

if predict:

    with st.spinner(
        "Analyzing using AI..."
    ):

        result = predict_all(

            artist=artist,

            album_type=album_type,

            duration_ms=duration,

            total_tracks=tracks,

            is_explicit=explicit,

            release_year=year,

            release_month=month

        )


    st.success(
        "Prediction Completed Successfully!"
    )

    st.divider()


    # ======================================================
    # MAIN PREDICTION RESULTS
    # ======================================================

    c1, c2, c3, c4 = st.columns(4)


    # ------------------------------------------------------
    # POPULARITY
    # ------------------------------------------------------

    with c1:

        st.metric(
            "⭐ Popularity",
            f'{result["Popularity Score"]:.2f}'
        )


    # ------------------------------------------------------
    # TRENDING
    # ------------------------------------------------------

    with c2:

        st.metric(
            "🔥 Trending",
            result["Trending"]
        )


    # ------------------------------------------------------
    # TOP 10
    # ------------------------------------------------------

    with c3:

        st.metric(
            "🏆 Top 10",
            result["Top10 Prediction"]
        )


    # ------------------------------------------------------
    # ARTIST SCORE
    # ------------------------------------------------------

    with c4:

        st.metric(
            "👑 Artist Score",
            f'{result["Artist Success Score"]:.2f}'
        )


    st.write("")


    # ======================================================
    # AI CONFIDENCE
    # ======================================================

    st.subheader(
        "📊 AI Confidence"
    )


    # ------------------------------------------------------
    # TRENDING CONFIDENCE
    # ------------------------------------------------------

    st.write(
        "🔥 Trending Confidence"
    )

    trending_confidence = int(
        result.get(
            "Trending Confidence",
            0
        )
    )

    st.progress(
        max(
            0,
            min(
                trending_confidence,
                100
            )
        )
    )

    st.caption(
        f"{trending_confidence}%"
    )


    st.write("")


    # ------------------------------------------------------
    # TOP 10 CONFIDENCE
    # ------------------------------------------------------

    st.write(
        "🏆 Top 10 Confidence"
    )

    top10_confidence = int(
        result.get(
            "Top10 Confidence",
            0
        )
    )

    st.progress(
        max(
            0,
            min(
                top10_confidence,
                100
            )
        )
    )

    st.caption(
        f"{top10_confidence}%"
    )


    st.write("")


    # ------------------------------------------------------
    # POPULARITY SCORE
    # ------------------------------------------------------

    popularity = float(
        result["Popularity Score"]
    )

    st.write(
        "⭐ Popularity Score"
    )

    st.progress(
        max(
            0,
            min(
                int(popularity),
                100
            )
        )
    )

    st.caption(
        f"{popularity:.1f}/100"
    )


    st.write("")


    # ------------------------------------------------------
    # ARTIST SUCCESS SCORE
    # ------------------------------------------------------

    artist_score = float(
        result["Artist Success Score"]
    )

    st.write(
        "👑 Artist Success Score"
    )

    st.progress(
        max(
            0,
            min(
                int(artist_score),
                100
            )
        )
    )

    st.caption(
        f"{artist_score:.1f}/100"
    )


    st.divider()


    # ======================================================
    # AI INSIGHTS
    # ======================================================

    st.subheader(
        "🤖 AI Insights"
    )


    # ------------------------------------------------------
    # POPULARITY INSIGHT
    # ------------------------------------------------------

    if popularity >= 90:

        st.success(
            "⭐ This song has outstanding commercial potential."
        )

    elif popularity >= 80:

        st.success(
            "⭐ This song is expected to perform very well."
        )

    elif popularity >= 70:

        st.info(
            "⭐ The song has good potential with proper promotion."
        )

    else:

        st.warning(
            "⭐ Popularity is predicted to be moderate."
        )


    # ------------------------------------------------------
    # TRENDING INSIGHT
    # ------------------------------------------------------

    trending_value = str(
        result["Trending"]
    )

    if trending_value.startswith("Yes"):

        st.success(
            "🔥 The model predicts this song will likely become trending."
        )

    else:

        st.info(
            "🔥 Trending probability is currently low."
        )


    # ------------------------------------------------------
    # TOP 10 INSIGHT
    # ------------------------------------------------------

    top10_value = str(
        result["Top10 Prediction"]
    )

    if top10_value.startswith("Yes"):

        st.success(
            "🏆 Strong probability of reaching the Top 10."
        )

    else:

        st.warning(
            "🏆 Entering the Top 10 may require additional marketing."
        )


    # ------------------------------------------------------
    # ARTIST GRADE
    # ------------------------------------------------------

    artist_grade = result.get(
        "Artist Grade",
        "N/A"
    )

    st.info(
        f"👑 Artist Grade : {artist_grade}"
    )


    st.divider()


    # ======================================================
    # PREDICTION SUMMARY
    # ======================================================

    st.subheader(
        "📋 Prediction Summary"
    )


    summary = pd.DataFrame({

        "Prediction": [

            "Popularity",

            "Trending",

            "Trending Confidence",

            "Top 10",

            "Top 10 Confidence",

            "Artist Success",

            "Artist Grade"

        ],

        "Result": [

            result["Popularity Score"],

            result["Trending"],

            f"{trending_confidence}%",

            result["Top10 Prediction"],

            f"{top10_confidence}%",

            result["Artist Success Score"],

            artist_grade

        ]

    })


    st.dataframe(

        summary,

        use_container_width=True,

        hide_index=True

    )


    st.divider()


    # ======================================================
    # DOWNLOAD PREDICTION REPORT
    # ======================================================

    st.subheader(
        "📥 Download Prediction Report"
    )


    report = pd.DataFrame({

        "Artist": [
            artist
        ],

        "Song": [
            song
        ],

        "Album Type": [
            album_type
        ],

        "Duration (ms)": [
            duration
        ],

        "Tracks": [
            tracks
        ],

        "Explicit": [
            explicit
        ],

        "Release Year": [
            year
        ],

        "Release Month": [
            month
        ],

        "Popularity Prediction": [
            result["Popularity Score"]
        ],

        "Trending": [
            result["Trending"]
        ],

        "Trending Confidence": [
            trending_confidence
        ],

        "Top10 Prediction": [
            result["Top10 Prediction"]
        ],

        "Top10 Confidence": [
            top10_confidence
        ],

        "Artist Success Score": [
            result["Artist Success Score"]
        ],

        "Artist Grade": [
            artist_grade
        ]

    })


    csv = report.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(

        "⬇ Download Prediction Report",

        csv,

        "prediction_report.csv",

        "text/csv",

        key="download_prediction",

        use_container_width=True

    )


    st.divider()


    # ======================================================
    # OVERALL PERFORMANCE SCORE
    # ======================================================

    st.subheader(
        "🎯 Overall Performance Score"
    )


    overall = round(

        (

            float(
                result["Popularity Score"]
            )

            +

            float(
                result["Artist Success Score"]
            )

            +

            trending_confidence

            +

            top10_confidence

        ) / 4,

        2

    )


    st.progress(

        max(
            0,
            min(
                int(overall),
                100
            )
        )

    )


    st.metric(

        "Overall AI Score",

        f"{overall}/100"

    )


    if overall >= 90:

        st.success(
            "⭐⭐⭐⭐⭐ Outstanding Prediction"
        )

    elif overall >= 80:

        st.success(
            "⭐⭐⭐⭐ Excellent Prediction"
        )

    elif overall >= 70:

        st.info(
            "⭐⭐⭐ Good Prediction"
        )

    else:

        st.warning(
            "⭐⭐ Average Prediction"
        )


    st.divider()


# ==========================================================
# FOOTER
# ==========================================================

st.markdown("""

<center>

<h2>🎵 K-Wave Analytics</h2>

<p>
AI-Powered K-Pop Trend Intelligence Platform
</p>

<p>
Built with ❤️ using
<br>
Python • Streamlit • Plotly • Pandas • Scikit-Learn
</p>

<p style="color:gray;">
Version 1.0 • © 2026
</p>

</center>

""", unsafe_allow_html=True)