"""
=========================================================
K-Wave Analytics
Feature Engineering
=========================================================

Input:
    data/cleaned_data.csv

Outputs:
    data/ml_dataset.csv
    data/artist_summary.csv
    data/trend_data.csv

    models/artist_encoder.pkl
    models/album_encoder.pkl
"""

import os
import joblib
import pandas as pd

from sklearn.preprocessing import LabelEncoder


# ==========================================================
# Configuration
# ==========================================================

INPUT_FILE = "data/cleaned_data.csv"

ML_DATASET = "data/ml_dataset.csv"

ARTIST_SUMMARY = "data/artist_summary.csv"

TREND_DATA = "data/trend_data.csv"

MODELS_FOLDER = "models"


# ==========================================================
# Load Dataset
# ==========================================================

def load_dataset():

    print("=" * 60)
    print("Loading Clean Dataset")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)

    return df


# ==========================================================
# Label Encoding
# ==========================================================

def encode_features(df):

    print("\nEncoding Features...")

    os.makedirs(MODELS_FOLDER, exist_ok=True)

    artist_encoder = LabelEncoder()

    album_encoder = LabelEncoder()

    df["artist_encoded"] = artist_encoder.fit_transform(
        df["artist"]
    )

    df["album_type_encoded"] = album_encoder.fit_transform(
        df["album_type"]
    )

    joblib.dump(
        artist_encoder,
        os.path.join(
            MODELS_FOLDER,
            "artist_encoder.pkl"
        )
    )

    joblib.dump(
        album_encoder,
        os.path.join(
            MODELS_FOLDER,
            "album_encoder.pkl"
        )
    )

    print("✓ Encoders Saved")

    return df


# ==========================================================
# Trending Label
# ==========================================================

def create_trending_label(df):

    print("Creating Trending Label...")

    df["trending_label"] = (
        df["popularity"] >= 80
    ).astype(int)

    return df


# ==========================================================
# Top 10 Label
# ==========================================================

def create_top10_label(df):

    print("Creating Top 10 Label...")

    df["top10_label"] = (
        df["position"] <= 10
    ).astype(int)

    return df


# ==========================================================
# Artist Success Score
# ==========================================================

def create_artist_success(df):

    print("Creating Artist Success Score...")

    artist_avg = (
        df.groupby("artist")["popularity"]
        .mean()
        .to_dict()
    )

    df["artist_success_score"] = (
        df["artist"]
        .map(artist_avg)
        .round(2)
    )

    return df


# ==========================================================
# Release Features
# ==========================================================

def create_release_features(df):

    print("Creating Date Features...")

    df["release_year"] = df["year"]

    df["release_month"] = df["month"]

    return df


# ==========================================================
# Artist Summary
# ==========================================================

def create_artist_summary(df):

    print("Creating Artist Summary...")

    summary = (

        df.groupby("artist")

        .agg(

            total_songs=("song", "count"),

            average_popularity=("popularity", "mean"),

            max_popularity=("popularity", "max"),

            average_duration=("duration_minutes", "mean"),

            average_tracks=("total_tracks", "mean"),

            success_score=("artist_success_score", "mean")

        )

        .reset_index()

    )

    summary = summary.round(2)

    summary.to_csv(

        ARTIST_SUMMARY,

        index=False

    )

    print("✓ artist_summary.csv Saved")


# ==========================================================
# Trend Data
# ==========================================================

def create_trend_data(df):

    print("Creating Trend Data...")

    trend = (

        df.groupby(

            ["release_year", "release_month"]

        )

        .agg(

            average_popularity=("popularity", "mean"),

            total_songs=("song", "count"),

            trending_songs=("trending_label", "sum")

        )

        .reset_index()

    )

    trend = trend.round(2)

    trend.to_csv(

        TREND_DATA,

        index=False

    )

    print("✓ trend_data.csv Saved")


# ==========================================================
# Save ML Dataset
# ==========================================================

def save_dataset(df):

    df.to_csv(

        ML_DATASET,

        index=False

    )

    print("✓ ml_dataset.csv Saved")


# ==========================================================
# Main
# ==========================================================

def main():

    df = load_dataset()

    df = encode_features(df)

    df = create_trending_label(df)

    df = create_top10_label(df)

    df = create_artist_success(df)

    df = create_release_features(df)

    create_artist_summary(df)

    create_trend_data(df)

    save_dataset(df)

    print("\n" + "=" * 60)

    print("Feature Engineering Completed Successfully")

    print("=" * 60)


if __name__ == "__main__":

    main()