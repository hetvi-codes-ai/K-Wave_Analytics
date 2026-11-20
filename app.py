import streamlit as st
import pandas as pd
import plotly.express as px

from src.utils import load_data
from src.predict import predict_all

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="K-Wave Analytics",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

.main{
    background:#0E1117;
}

.block-container{
    padding-top:1rem;
}

.hero{

background:linear-gradient(135deg,#6C63FF,#8E44AD);

padding:35px;

border-radius:20px;

text-align:center;

color:white;

}

.metric-card{

background:#1E1E1E;

padding:20px;

border-radius:15px;

border:1px solid #333;

text-align:center;

}

.metric-title{

font-size:16px;

color:#BBBBBB;

}

.metric-value{

font-size:34px;

font-weight:bold;

color:white;

}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# LOAD DATA
# ==========================================================

df = load_data()

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.image(
    "assets/logo.png",
    width=120
)

st.sidebar.title("🎵 K-Wave Analytics")

st.sidebar.markdown("---")

st.sidebar.success("AI-Powered K-Pop Trend Intelligence")

st.sidebar.markdown("---")

st.sidebar.caption("Version 1.0")

# ==========================================================
# HERO SECTION
# ==========================================================

st.markdown("""

<div class="hero">

<h1>🎵 K-Wave Analytics</h1>

<h3>AI-Powered K-Pop Trend Intelligence Platform</h3>

<p>

Analyze Songs • Predict Popularity • Find Trends •
Recommend Music Using Machine Learning

</p>

</div>

""", unsafe_allow_html=True)

st.write("")

# ==========================================================
# KPI CARDS
# ==========================================================

songs = len(df)

artists = df["artist"].nunique()

avg_popularity = round(df["popularity"].mean(),2)

trending = len(df[df["trending_label"]==1])

c1,c2,c3,c4 = st.columns(4)

with c1:

    st.markdown(f"""

<div class="metric-card">

<div class="metric-title">

🎵 Songs

</div>

<div class="metric-value">

{songs}

</div>

</div>

""",unsafe_allow_html=True)

with c2:

    st.markdown(f"""

<div class="metric-card">

<div class="metric-title">

👨‍🎤 Artists

</div>

<div class="metric-value">

{artists}

</div>

</div>

""",unsafe_allow_html=True)

with c3:

    st.markdown(f"""

<div class="metric-card">

<div class="metric-title">

⭐ Avg Popularity

</div>

<div class="metric-value">

{avg_popularity}

</div>

</div>

""",unsafe_allow_html=True)

with c4:

    st.markdown(f"""

<div class="metric-card">

<div class="metric-title">

🔥 Trending Songs

</div>

<div class="metric-value">

{trending}

</div>

</div>

""",unsafe_allow_html=True)

st.divider()

# ==========================================================
# QUICK OVERVIEW
# ==========================================================

left,right = st.columns(2)

with left:

    st.subheader("🏆 Top 10 Artists")

    top_artist = (

        df.groupby("artist")["popularity"]

        .mean()

        .sort_values(ascending=False)

        .head(10)

        .reset_index()

    )

    fig = px.bar(

        top_artist,

        x="popularity",

        y="artist",

        orientation="h",

        color="popularity",

        text="popularity"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with right:

    st.subheader("🎵 Album Distribution")

    fig2 = px.pie(

        df,

        names="album_type"

    )

    st.plotly_chart(

        fig2,

        use_container_width=True

    )

st.divider()
# ==========================================================
# SEARCH SONG
# ==========================================================

st.subheader("🔍 Search K-Pop Songs")

search = st.text_input(
    "Enter Song or Artist Name"
)

if search:

    filtered = df[
        df["song"].str.contains(search, case=False, na=False)
        |
        df["artist"].str.contains(search, case=False, na=False)
    ]

    st.dataframe(
        filtered[
            [
                "song",
                "artist",
                "album_type",
                "popularity",
                "position"
            ]
        ],
        use_container_width=True
    )

st.divider()

# ==========================================================
# MONTHLY TREND
# ==========================================================

st.subheader("📈 Monthly Music Trends")

monthly = (

    df.groupby("release_month")["popularity"]

    .mean()

    .reset_index()

)

fig = px.line(

    monthly,

    x="release_month",

    y="popularity",

    markers=True,

    title="Average Popularity by Month"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

# ==========================================================
# TOP TRENDING SONGS
# ==========================================================

st.subheader("🔥 Top Trending Songs")

top_trending = (

    df.sort_values(

        "popularity",

        ascending=False

    )

    .head(10)

)

st.dataframe(

    top_trending[

        [

            "song",

            "artist",

            "popularity",

            "position"

        ]

    ],

    use_container_width=True,

    hide_index=True

)

st.divider()

# ==========================================================
# FEATURED ARTISTS
# ==========================================================

st.subheader("👨‍🎤 Featured Artists")

top_artists = (

    df.groupby("artist")

    .agg({

        "popularity":"mean",

        "song":"count"

    })

    .reset_index()

)

top_artists.columns = [

    "Artist",

    "Average Popularity",

    "Songs"

]

top_artists = top_artists.sort_values(

    "Average Popularity",

    ascending=False

).head(10)

st.dataframe(

    top_artists,

    use_container_width=True,

    hide_index=True

)

st.divider()

# ==========================================================
# PROJECT FEATURES
# ==========================================================

st.subheader("✨ Platform Features")

col1, col2 = st.columns(2)

with col1:

    st.success("📊 Interactive Analytics")

    st.success("🤖 AI Predictions")

    st.success("🎵 Music Recommendation")

    st.success("📈 Trend Analysis")

with col2:

    st.success("⭐ Popularity Prediction")

    st.success("🔥 Trending Detection")

    st.success("🏆 Top10 Prediction")

    st.success("👑 Artist Success Prediction")

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("""

<center>

## 🎵 K-Wave Analytics

### AI-Powered K-Pop Trend Intelligence Platform

Built with ❤️ using

Python • Streamlit • Scikit-Learn • Plotly • Pandas

© 2026

</center>

""", unsafe_allow_html=True)