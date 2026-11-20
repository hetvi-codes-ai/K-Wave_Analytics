"""
=========================================================
K-Wave Analytics
Charts Module
=========================================================
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ==========================================================
# Top Artists Chart
# ==========================================================

def top_artists_chart(df):

    artist_df = (
        df.groupby("artist")["popularity"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        artist_df,
        x="popularity",
        y="artist",
        orientation="h",
        color="popularity",
        text="popularity",
        color_continuous_scale="Plasma",
        title="Top 10 Artists by Popularity"
    )

    fig.update_layout(
        template="plotly_dark",
        title_x=0.5,
        height=550,
        xaxis_title="Popularity",
        yaxis_title="Artist"
    )

    return fig


# ==========================================================
# Top Songs Chart
# ==========================================================

def top_songs_chart(df):

    songs = (
        df.sort_values("popularity", ascending=False)
        .head(10)
    )

    fig = px.bar(
        songs,
        x="popularity",
        y="song",
        orientation="h",
        color="popularity",
        text="popularity",
        hover_data=["artist"],
        color_continuous_scale="Turbo",
        title="Top 10 Songs"
    )

    fig.update_layout(
        template="plotly_dark",
        title_x=0.5,
        height=550,
        xaxis_title="Popularity",
        yaxis_title="Song"
    )

    return fig


# ==========================================================
# Album Distribution
# ==========================================================

def album_distribution_chart(df):

    fig = px.pie(
        df,
        names="album_type",
        hole=0.45,
        title="Album Type Distribution"
    )

    fig.update_layout(
        template="plotly_dark",
        title_x=0.5,
        height=500
    )

    return fig


# ==========================================================
# Popularity Distribution
# ==========================================================

def popularity_distribution(df):

    fig = px.histogram(
        df,
        x="popularity",
        nbins=25,
        color="album_type",
        title="Popularity Distribution"
    )

    fig.update_layout(
        template="plotly_dark",
        title_x=0.5,
        bargap=0.05
    )

    return fig


# ==========================================================
# Monthly Trend
# ==========================================================

def monthly_trend(df):

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
        title="Monthly Popularity Trend"
    )

    fig.update_layout(
        template="plotly_dark",
        title_x=0.5,
        xaxis_title="Month",
        yaxis_title="Average Popularity"
    )

    return fig


# ==========================================================
# Yearly Trend
# ==========================================================

def yearly_trend(df):

    yearly = (
        df.groupby("release_year")["popularity"]
        .mean()
        .reset_index()
    )

    fig = px.line(
        yearly,
        x="release_year",
        y="popularity",
        markers=True,
        title="Yearly Popularity Trend"
    )

    fig.update_layout(
        template="plotly_dark",
        title_x=0.5,
        xaxis_title="Year",
        yaxis_title="Average Popularity"
    )

    return fig


# ==========================================================
# Compare Artists
# ==========================================================

def compare_artists(df, artists):

    compare = (
        df[df["artist"].isin(artists)]
        .groupby("artist")["popularity"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        compare,
        x="artist",
        y="popularity",
        color="artist",
        text="popularity",
        title="Artist Comparison"
    )

    fig.update_layout(
        template="plotly_dark",
        title_x=0.5
    )

    return fig

# ==========================================================
# Correlation Heatmap
# ==========================================================

def correlation_heatmap(df):

    columns = [
        "popularity",
        "duration_minutes",
        "total_tracks",
        "release_year",
        "release_month"
    ]

    corr = df[columns].corr(numeric_only=True)

    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        title="Feature Correlation Heatmap"
    )

    fig.update_layout(
        template="plotly_dark",
        title_x=0.5,
        height=650
    )

    return fig


# ==========================================================
# Artist Success Chart
# ==========================================================

def artist_success_chart(df):

    artist_df = (

        df.groupby("artist")["artist_success_score"]

        .mean()

        .reset_index()

        .sort_values(
            "artist_success_score",
            ascending=False
        )

        .head(15)

    )

    fig = px.bar(

        artist_df,

        x="artist_success_score",

        y="artist",

        orientation="h",

        color="artist_success_score",

        text="artist_success_score",

        color_continuous_scale="Viridis",

        title="Top Artist Success Score"

    )

    fig.update_layout(

        template="plotly_dark",

        title_x=0.5,

        height=600,

        xaxis_title="Success Score",

        yaxis_title="Artist"

    )

    return fig


# ==========================================================
# Song Duration vs Popularity
# ==========================================================

def artist_scatter(df):

    fig = px.scatter(

        df,

        x="duration_minutes",

        y="popularity",

        color="artist",

        hover_name="song",

        size="popularity",

        title="Song Duration vs Popularity"

    )

    fig.update_layout(

        template="plotly_dark",

        title_x=0.5,

        height=600

    )

    return fig


# ==========================================================
# Recommendation Similarity
# ==========================================================

def similarity_chart(recommendations):

    fig = px.bar(

        recommendations,

        x="Similarity",

        y="Song",

        orientation="h",

        color="Similarity",

        text="Similarity",

        color_continuous_scale="Turbo",

        title="Recommended Songs Similarity"

    )

    fig.update_layout(

        template="plotly_dark",

        title_x=0.5,

        height=550,

        xaxis_title="Similarity (%)",

        yaxis_title="Song"

    )

    return fig


# ==========================================================
# Popularity vs Similarity
# ==========================================================

def popularity_comparison(recommendations):

    fig = px.scatter(

        recommendations,

        x="Similarity",

        y="Popularity",

        color="Artist",

        hover_name="Song",

        size="Popularity",

        title="Popularity vs Similarity"

    )

    fig.update_layout(

        template="plotly_dark",

        title_x=0.5,

        height=550

    )

    return fig


# ==========================================================
# Popularity Gauge
# ==========================================================

def popularity_gauge(score):

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=score,

            title={"text": "Popularity Score"},

            gauge={

                "axis": {"range": [0, 100]},

                "bar": {"color": "#6C63FF"},

                "steps": [

                    {"range": [0, 30], "color": "#3A3A3A"},

                    {"range": [30, 70], "color": "#5A4FCF"},

                    {"range": [70, 100], "color": "#8E44AD"}

                ]

            }

        )

    )

    fig.update_layout(

        template="plotly_dark",

        height=350

    )

    return fig


# ==========================================================
# Confidence Gauge
# ==========================================================

def confidence_gauge(value, title="Confidence"):

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=value,

            title={"text": title},

            gauge={

                "axis": {"range": [0, 100]},

                "bar": {"color": "#00CC96"},

                "steps": [

                    {"range": [0, 40], "color": "#3A3A3A"},

                    {"range": [40, 70], "color": "#2D8C74"},

                    {"range": [70, 100], "color": "#00CC96"}

                ]

            }

        )

    )

    fig.update_layout(

        template="plotly_dark",

        height=350

    )

    return fig


# ==========================================================
# Explicit vs Non-Explicit Songs
# ==========================================================

def explicit_chart(df):

    explicit = (

        df.groupby("is_explicit")

        .size()

        .reset_index(name="Count")

    )

    explicit["is_explicit"] = explicit["is_explicit"].replace({

        0: "Non Explicit",

        1: "Explicit",

        False: "Non Explicit",

        True: "Explicit"

    })

    fig = px.pie(

        explicit,

        names="is_explicit",

        values="Count",

        hole=0.45,

        title="Explicit Songs Distribution"

    )

    fig.update_layout(

        template="plotly_dark",

        title_x=0.5,

        height=500

    )

    return fig


# ==========================================================
# Average Popularity by Album Type
# ==========================================================

def album_popularity_chart(df):

    album = (

        df.groupby("album_type")["popularity"]

        .mean()

        .reset_index()

    )

    fig = px.bar(

        album,

        x="album_type",

        y="popularity",

        color="album_type",

        text="popularity",

        title="Average Popularity by Album Type"

    )

    fig.update_layout(

        template="plotly_dark",

        title_x=0.5,

        height=500

    )

    return fig