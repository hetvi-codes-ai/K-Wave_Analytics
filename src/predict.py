"""
=========================================================
K-Wave Analytics
AI Prediction Engine
=========================================================

Models used:
    popularity_model.pkl
    trending_model.pkl
    top10_model.pkl
    artist_success_model.pkl

Encoders used:
    artist_encoder.pkl
    album_encoder.pkl

Predictions:
    1. Popularity Score
    2. Trending Prediction
    3. Trending Confidence
    4. Top 10 Prediction
    5. Top 10 Confidence
    6. Artist Success Score
    7. Artist Grade
=========================================================
"""

import os
import joblib
import pandas as pd


# =========================================================
# MODEL FOLDER
# =========================================================

MODEL_FOLDER = "models"


# =========================================================
# MODEL PATHS
# =========================================================

POPULARITY_MODEL = os.path.join(
    MODEL_FOLDER,
    "popularity_model.pkl"
)

TRENDING_MODEL = os.path.join(
    MODEL_FOLDER,
    "trending_model.pkl"
)

TOP10_MODEL = os.path.join(
    MODEL_FOLDER,
    "top10_model.pkl"
)

ARTIST_MODEL = os.path.join(
    MODEL_FOLDER,
    "artist_success_model.pkl"
)


# =========================================================
# ENCODER PATHS
# =========================================================

ARTIST_ENCODER = os.path.join(
    MODEL_FOLDER,
    "artist_encoder.pkl"
)

ALBUM_ENCODER = os.path.join(
    MODEL_FOLDER,
    "album_encoder.pkl"
)


# =========================================================
# LOAD MODELS
# =========================================================

try:

    popularity_model = joblib.load(
        POPULARITY_MODEL
    )

    trending_model = joblib.load(
        TRENDING_MODEL
    )

    top10_model = joblib.load(
        TOP10_MODEL
    )

    artist_model = joblib.load(
        ARTIST_MODEL
    )

    artist_encoder = joblib.load(
        ARTIST_ENCODER
    )

    album_encoder = joblib.load(
        ALBUM_ENCODER
    )

except Exception as e:

    raise RuntimeError(
        f"Error loading AI models: {e}"
    )


# =========================================================
# SAFE ARTIST ENCODING
# =========================================================

def encode_artist(artist):

    try:

        if artist in artist_encoder.classes_:

            return artist_encoder.transform(
                [artist]
            )[0]

        return 0

    except Exception:

        return 0


# =========================================================
# SAFE ALBUM ENCODING
# =========================================================

def encode_album(album):

    try:

        if album in album_encoder.classes_:

            return album_encoder.transform(
                [album]
            )[0]

        return 0

    except Exception:

        return 0


# =========================================================
# BUILD FEATURES
# =========================================================

def build_features(
    artist,
    album_type,
    duration_ms,
    total_tracks,
    is_explicit,
    release_year,
    release_month
):

    artist_encoded = encode_artist(
        artist
    )

    album_encoded = encode_album(
        album_type
    )

    features = pd.DataFrame({

        "artist_encoded": [
            artist_encoded
        ],

        "album_type_encoded": [
            album_encoded
        ],

        "duration_ms": [
            duration_ms
        ],

        "total_tracks": [
            total_tracks
        ],

        "is_explicit": [
            int(is_explicit)
        ],

        "release_year": [
            release_year
        ],

        "release_month": [
            release_month
        ]

    })

    return features


# =========================================================
# POPULARITY PREDICTION
# =========================================================

def predict_popularity(
    artist,
    album_type,
    duration_ms,
    total_tracks,
    is_explicit,
    release_year,
    release_month
):

    X = build_features(
        artist,
        album_type,
        duration_ms,
        total_tracks,
        is_explicit,
        release_year,
        release_month
    )

    prediction = popularity_model.predict(
        X
    )[0]

    prediction = float(
        prediction
    )

    prediction = max(
        0,
        min(100, prediction)
    )

    return round(
        prediction,
        2
    )


# =========================================================
# TRENDING PREDICTION
# =========================================================

def predict_trending(
    artist,
    album_type,
    duration_ms,
    total_tracks,
    is_explicit,
    release_year,
    release_month
):

    X = build_features(
        artist,
        album_type,
        duration_ms,
        total_tracks,
        is_explicit,
        release_year,
        release_month
    )

    prediction = trending_model.predict(
        X
    )[0]

    if prediction == 1:

        return "Yes"

    return "No"


# =========================================================
# TRENDING CONFIDENCE
# =========================================================

def predict_trending_confidence(
    artist,
    album_type,
    duration_ms,
    total_tracks,
    is_explicit,
    release_year,
    release_month
):

    X = build_features(
        artist,
        album_type,
        duration_ms,
        total_tracks,
        is_explicit,
        release_year,
        release_month
    )

    prediction = trending_model.predict(
        X
    )[0]

    if hasattr(
        trending_model,
        "predict_proba"
    ):

        probabilities = (
            trending_model
            .predict_proba(X)[0]
        )

        confidence = max(
            probabilities
        ) * 100

    else:

        confidence = (
            100
            if prediction == 1
            else 50
        )

    confidence = max(
        0,
        min(100, confidence)
    )

    return round(
        float(confidence),
        2
    )


# =========================================================
# TOP 10 PREDICTION
# =========================================================

def predict_top10(
    artist,
    album_type,
    duration_ms,
    total_tracks,
    is_explicit,
    release_year,
    release_month
):

    X = build_features(
        artist,
        album_type,
        duration_ms,
        total_tracks,
        is_explicit,
        release_year,
        release_month
    )

    prediction = top10_model.predict(
        X
    )[0]

    if prediction == 1:

        return "Yes"

    return "No"


# =========================================================
# TOP 10 CONFIDENCE
# =========================================================

def predict_top10_confidence(
    artist,
    album_type,
    duration_ms,
    total_tracks,
    is_explicit,
    release_year,
    release_month
):

    X = build_features(
        artist,
        album_type,
        duration_ms,
        total_tracks,
        is_explicit,
        release_year,
        release_month
    )

    prediction = top10_model.predict(
        X
    )[0]

    if hasattr(
        top10_model,
        "predict_proba"
    ):

        probabilities = (
            top10_model
            .predict_proba(X)[0]
        )

        confidence = max(
            probabilities
        ) * 100

    else:

        confidence = (
            100
            if prediction == 1
            else 50
        )

    confidence = max(
        0,
        min(100, confidence)
    )

    return round(
        float(confidence),
        2
    )


# =========================================================
# ARTIST SUCCESS PREDICTION
# =========================================================

def predict_artist_success(
    artist,
    album_type,
    duration_ms,
    total_tracks,
    is_explicit,
    release_year,
    release_month
):

    X = build_features(
        artist,
        album_type,
        duration_ms,
        total_tracks,
        is_explicit,
        release_year,
        release_month
    )

    prediction = artist_model.predict(
        X
    )[0]

    prediction = float(
        prediction
    )

    prediction = max(
        0,
        min(100, prediction)
    )

    return round(
        prediction,
        2
    )


# =========================================================
# ARTIST GRADE
# =========================================================

def get_artist_grade(
    artist_score
):

    if artist_score >= 90:

        return "S"

    elif artist_score >= 80:

        return "A"

    elif artist_score >= 70:

        return "B"

    elif artist_score >= 60:

        return "C"

    else:

        return "D"


# =========================================================
# PREDICT EVERYTHING
# =========================================================

def predict_all(
    artist,
    album_type,
    duration_ms,
    total_tracks,
    is_explicit,
    release_year,
    release_month
):

    # -----------------------------------------------------
    # Build feature data
    # -----------------------------------------------------

    X = build_features(
        artist,
        album_type,
        duration_ms,
        total_tracks,
        is_explicit,
        release_year,
        release_month
    )

    # =====================================================
    # POPULARITY
    # =====================================================

    popularity = popularity_model.predict(
        X
    )[0]

    popularity = float(
        popularity
    )

    popularity = max(
        0,
        min(100, popularity)
    )

    popularity = round(
        popularity,
        2
    )

    # =====================================================
    # TRENDING
    # =====================================================

    trend_prediction = trending_model.predict(
        X
    )[0]

    trending = (
        "Yes"
        if trend_prediction == 1
        else "No"
    )

    # -----------------------------------------------------
    # Trending Confidence
    # -----------------------------------------------------

    if hasattr(
        trending_model,
        "predict_proba"
    ):

        probabilities = (
            trending_model
            .predict_proba(X)[0]
        )

        trending_confidence = (
            max(probabilities) * 100
        )

    else:

        trending_confidence = (
            100
            if trend_prediction == 1
            else 50
        )

    trending_confidence = max(
        0,
        min(
            100,
            trending_confidence
        )
    )

    trending_confidence = round(
        float(trending_confidence),
        2
    )

    # =====================================================
    # TOP 10
    # =====================================================

    top10_prediction = top10_model.predict(
        X
    )[0]

    top10 = (
        "Yes"
        if top10_prediction == 1
        else "No"
    )

    # -----------------------------------------------------
    # Top 10 Confidence
    # -----------------------------------------------------

    if hasattr(
        top10_model,
        "predict_proba"
    ):

        probabilities = (
            top10_model
            .predict_proba(X)[0]
        )

        top10_confidence = (
            max(probabilities) * 100
        )

    else:

        top10_confidence = (
            100
            if top10_prediction == 1
            else 50
        )

    top10_confidence = max(
        0,
        min(
            100,
            top10_confidence
        )
    )

    top10_confidence = round(
        float(top10_confidence),
        2
    )

    # =====================================================
    # ARTIST SUCCESS
    # =====================================================

    artist_score = artist_model.predict(
        X
    )[0]

    artist_score = float(
        artist_score
    )

    artist_score = max(
        0,
        min(100, artist_score)
    )

    artist_score = round(
        artist_score,
        2
    )

    # =====================================================
    # ARTIST GRADE
    # =====================================================

    artist_grade = get_artist_grade(
        artist_score
    )

    # =====================================================
    # RETURN RESULTS
    # =====================================================

    return {

        "Popularity Score":
            popularity,

        "Trending":
            trending,

        "Trending Confidence":
            trending_confidence,

        "Top10 Prediction":
            top10,

        "Top10 Confidence":
            top10_confidence,

        "Artist Success Score":
            artist_score,

        "Artist Grade":
            artist_grade

    }


# =========================================================
# DASHBOARD WRAPPER
# =========================================================

def predict_song(
    artist,
    album_type,
    duration_ms,
    total_tracks,
    is_explicit,
    release_year,
    release_month
):

    return predict_all(

        artist=artist,

        album_type=album_type,

        duration_ms=duration_ms,

        total_tracks=total_tracks,

        is_explicit=is_explicit,

        release_year=release_year,

        release_month=release_month

    )


# =========================================================
# TEST PREDICTION
# =========================================================

if __name__ == "__main__":

    print("=" * 60)

    print(
        "K-Wave Analytics Prediction Engine"
    )

    print("=" * 60)

    result = predict_all(

        artist="BTS",

        album_type="Album",

        duration_ms=210000,

        total_tracks=10,

        is_explicit=0,

        release_year=2024,

        release_month=5

    )

    print(
        "\nPrediction Results:\n"
    )

    for key, value in result.items():

        print(
            f"{key}: {value}"
        )

    print(
        "\nPrediction completed successfully!"
    )