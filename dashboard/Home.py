import streamlit as st
import pandas as pd
import plotly.express as px

from src.utils import *

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="K-Wave Analytics",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# LOAD CSS
# ==========================================

def load_css():

    with open("dashboard/styles/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# ==========================================
# LOAD DATA
# ==========================================

df = load_data()

summary = get_summary(df)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3659/3659784.png",
    width=100
)

st.sidebar.title("K-Wave Analytics")

st.sidebar.markdown("---")

st.sidebar.success("AI-Powered Music Intelligence")

st.sidebar.info(
"""
Dataset

Atlantic South Korea

27K+ Songs
"""
)

st.sidebar.markdown("---")

st.sidebar.caption("Version 1.0")

# ==========================================
# HEADER
# ==========================================

st.markdown(
"""
<div class="main-title">

🎵 K-Wave Analytics

</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div class="sub-title">

AI-Powered K-Pop Trend Intelligence Platform

Analyze • Predict • Discover

</div>
""",
unsafe_allow_html=True
)

# ==========================================
# KPI CARDS
# ==========================================

col1,col2,col3,col4 = st.columns(4)

with col1:

    st.metric(
        "🎵 Songs",
        summary["total_songs"]
    )

with col2:

    st.metric(
        "👨‍🎤 Artists",
        summary["total_artists"]
    )

with col3:

    st.metric(
        "⭐ Avg Popularity",
        summary["average_popularity"]
    )

with col4:

    st.metric(
        "🅴 Explicit",
        summary["explicit_songs"]
    )

st.divider()

# ==========================================
# SEARCH
# ==========================================

search = st.text_input(
    "🔍 Search Artist or Song"
)

if search:

    result = df[
        df["artist"].str.contains(
            search,
            case=False,
            na=False
        )
        |
        df["song"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

    st.dataframe(
        result,
        use_container_width=True
    )

st.divider()

# ==========================================
# CHARTS
# ==========================================

left,right = st.columns(2)

# Top Artists

artist = (
    df.groupby("artist")
    ["popularity"]
    .mean()
    .sort_values(
        ascending=False
    )
    .head(10)
    .reset_index()
)

fig = px.bar(
    artist,
    x="artist",
    y="popularity",
    color="popularity",
    title="Top 10 Artists"
)

left.plotly_chart(
    fig,
    use_container_width=True
)

# Album Types

album = (
    df["album_type"]
    .value_counts()
    .reset_index()
)

album.columns = [
    "Album Type",
    "Count"
]

fig2 = px.pie(
    album,
    values="Count",
    names="Album Type",
    title="Album Type Distribution"
)

right.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================
# Monthly Trend
# ==========================================

st.subheader("📈 Monthly Popularity Trend")

df["date"] = pd.to_datetime(df["date"])

monthly = (
    df.groupby(
        df["date"].dt.to_period("M")
    )["popularity"]
    .mean()
    .reset_index()
)

monthly["date"] = monthly["date"].astype(str)

fig3 = px.line(
    monthly,
    x="date",
    y="popularity",
    markers=True
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================================
# Popular Songs
# ==========================================

st.subheader("🔥 Top 10 Songs")

top = top_songs(df)

st.dataframe(
    top,
    use_container_width=True
)

# ==========================================
# Popularity Histogram
# ==========================================

fig4 = px.histogram(
    df,
    x="popularity",
    nbins=25,
    title="Popularity Distribution"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ==========================================
# Recent Dataset
# ==========================================

with st.expander("View Dataset"):

    st.dataframe(
        df.head(100),
        use_container_width=True
    )

# ==========================================
# FOOTER
# ==========================================

st.markdown(
"""
<div class="footer">

Developed using

Python • Streamlit • Plotly • Machine Learning

</div>
""",
unsafe_allow_html=True
)