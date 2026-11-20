import streamlit as st
import pandas as pd
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "ml_dataset.csv"
)

# ==========================================================
# Load Dataset
# ==========================================================

@st.cache_data
def load_data():

    if not os.path.exists(DATA_PATH):
        st.error(f"Dataset not found:\n{DATA_PATH}")
        st.stop()

    df = pd.read_csv(DATA_PATH)

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # ------------------------------------------------------
    # Create optional columns if missing
    # ------------------------------------------------------

    defaults = {
        "album_cover_url": "",
        "album_type": "Single",
        "duration_ms": 180000,
        "duration_minutes": 3,
        "total_tracks": 1,
        "is_explicit": 0,
        "release_year": 2024,
        "release_month": 1,
        "position": 0,
        "trending_label": 0,
        "top10_label": 0,
        "artist_success_score": 0
    }

    for col, value in defaults.items():
        if col not in df.columns:
            df[col] = value

    # Generate duration_minutes if only duration_ms exists
    if "duration_minutes" not in df.columns:
        df["duration_minutes"] = (
            df["duration_ms"] / 60000
        ).round(2)

    return df


# ==========================================================
# Dataset Summary
# ==========================================================

def dataset_summary(df):

    return {

        "songs": len(df),

        "artists": df["artist"].nunique(),

        "albums": df["album_type"].nunique(),

        "avg_popularity": round(
            df["popularity"].mean(), 2
        ),

        "max_popularity": df["popularity"].max(),

        "min_popularity": df["popularity"].min()

    }


# ==========================================================
# Top Artists
# ==========================================================

def top_artists(df, n=10):

    return (

        df.groupby("artist")["popularity"]

        .mean()

        .sort_values(ascending=False)

        .head(n)

        .reset_index()

    )


# ==========================================================
# Top Songs
# ==========================================================

def top_songs(df, n=10):

    return (

        df.sort_values(

            "popularity",

            ascending=False

        )

        .head(n)

    )


# ==========================================================
# Monthly Trends
# ==========================================================

def monthly_trends(df):

    return (

        df.groupby("release_month")["popularity"]

        .mean()

        .reset_index()

        .sort_values("release_month")

    )


# ==========================================================
# Artist Songs
# ==========================================================

def get_artist_songs(df, artist):

    return df[df["artist"] == artist]


# ==========================================================
# Song Details
# ==========================================================

def get_song(df, artist, song):

    result = df[
        (df["artist"] == artist)
        &
        (df["song"] == song)
    ]

    if len(result) == 0:
        return None

    return result.iloc[0]


# ==========================================================
# Format Popularity
# ==========================================================

def popularity_label(score):

    if score >= 90:
        return "⭐⭐⭐⭐⭐ Excellent"

    elif score >= 75:
        return "⭐⭐⭐⭐ Very Good"

    elif score >= 60:
        return "⭐⭐⭐ Good"

    elif score >= 40:
        return "⭐⭐ Average"

    else:
        return "⭐ Low"


# ==========================================================
# Safe Image
# ==========================================================

def show_album_cover(url):

    if isinstance(url, str) and url.startswith("http"):
        return url

    return "https://via.placeholder.com/300x300.png?text=No+Cover"