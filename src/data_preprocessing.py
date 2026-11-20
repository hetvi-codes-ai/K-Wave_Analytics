"""
=========================================================
K-Wave Analytics
Data Preprocessing
=========================================================

Input:
    data/Atlantic_South_Korea.csv

Output:
    data/cleaned_data.csv
"""

import pandas as pd
import numpy as np
import os


# =====================================================
# Configuration
# =====================================================

INPUT_FILE = "data/Atlantic_South_Korea.csv"
OUTPUT_FILE = "data/cleaned_data.csv"


# =====================================================
# Load Dataset
# =====================================================

def load_dataset(path):

    print("=" * 60)
    print("Loading Dataset...")
    print("=" * 60)

    df = pd.read_csv(path)

    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    return df


# =====================================================
# Remove Duplicate Records
# =====================================================

def remove_duplicates(df):

    before = len(df)

    df = df.drop_duplicates()

    after = len(df)

    print(f"Duplicates Removed : {before - after}")

    return df


# =====================================================
# Handle Missing Values
# =====================================================

def handle_missing_values(df):

    print("\nMissing Values Before Cleaning")
    print(df.isnull().sum())

    text_columns = [
        "song",
        "artist",
        "album_type",
        "album_cover_url"
    ]

    for col in text_columns:

        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    numeric_columns = [
        "popularity",
        "duration_ms",
        "total_tracks",
        "position"
    ]

    for col in numeric_columns:

        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    if "is_explicit" in df.columns:
        df["is_explicit"] = df["is_explicit"].fillna(False)

    return df


# =====================================================
# Clean Text Columns
# =====================================================

def clean_text(df):

    text_columns = [
        "song",
        "artist",
        "album_type"
    ]

    for col in text_columns:

        if col in df.columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
            )

    return df


# =====================================================
# Convert Date
# =====================================================

def process_date(df):

    df["date"] = pd.to_datetime(
        df["date"],
        dayfirst=True,
        errors="coerce"
    )

    df["year"] = df["date"].dt.year

    df["month"] = df["date"].dt.month

    df["day"] = df["date"].dt.day

    return df


# =====================================================
# Clean Numeric Columns
# =====================================================

def clean_numeric(df):

    df["popularity"] = (
        df["popularity"]
        .clip(0, 100)
        .astype(int)
    )

    df["position"] = (
        df["position"]
        .astype(int)
    )

    df["duration_ms"] = (
        df["duration_ms"]
        .astype(int)
    )

    df["total_tracks"] = (
        df["total_tracks"]
        .astype(int)
    )

    return df


# =====================================================
# Convert Boolean
# =====================================================

def clean_boolean(df):

    df["is_explicit"] = (
        df["is_explicit"]
        .astype(bool)
    )

    return df


# =====================================================
# Remove Invalid Records
# =====================================================

def remove_invalid_rows(df):

    df = df[df["song"] != "Unknown"]

    df = df[df["artist"] != "Unknown"]

    df = df[df["duration_ms"] > 0]

    df = df[df["total_tracks"] > 0]

    return df


# =====================================================
# Create Duration in Minutes
# =====================================================

def create_duration_minutes(df):

    df["duration_minutes"] = (
        df["duration_ms"] / 60000
    ).round(2)

    return df


# =====================================================
# Dataset Summary
# =====================================================

def print_summary(df):

    print("\n" + "=" * 60)

    print("Dataset Summary")

    print("=" * 60)

    print(f"Rows               : {len(df)}")
    print(f"Columns            : {len(df.columns)}")
    print(f"Unique Artists     : {df['artist'].nunique()}")
    print(f"Unique Songs       : {df['song'].nunique()}")
    print(f"Average Popularity : {df['popularity'].mean():.2f}")

    print("=" * 60)


# =====================================================
# Save Dataset
# =====================================================

def save_dataset(df):

    os.makedirs("data", exist_ok=True)

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nSaved Successfully -> {OUTPUT_FILE}")


# =====================================================
# Main Function
# =====================================================

def main():

    df = load_dataset(INPUT_FILE)

    df = remove_duplicates(df)

    df = handle_missing_values(df)

    df = clean_text(df)

    df = process_date(df)

    df = clean_numeric(df)

    df = clean_boolean(df)

    df = remove_invalid_rows(df)

    df = create_duration_minutes(df)

    print_summary(df)

    save_dataset(df)


if __name__ == "__main__":

    main()