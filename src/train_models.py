"""
=========================================================
K-Wave Analytics
Train Machine Learning Models
=========================================================

Models:
1. Popularity Prediction (Regression)
2. Trending Prediction (Classification)
3. Top10 Prediction (Classification)
4. Artist Success Prediction (Regression)
"""

import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.ensemble import (
    RandomForestRegressor,
    RandomForestClassifier
)

from sklearn.metrics import (
    accuracy_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ==========================================================
# Configuration
# ==========================================================

DATASET = "data/ml_dataset.csv"

MODEL_DIR = "models"

os.makedirs(MODEL_DIR, exist_ok=True)

# ==========================================================
# Load Dataset
# ==========================================================

df = pd.read_csv(DATASET)

# ==========================================================
# Features
# ==========================================================

FEATURES = [

    "artist_encoded",

    "album_type_encoded",

    "duration_ms",

    "total_tracks",

    "is_explicit",

    "release_year",

    "release_month"

]

X = df[FEATURES]

# ==========================================================
# Metrics Storage
# ==========================================================

metrics = []

# ==========================================================
# Helper Functions
# ==========================================================

def save_metrics(model_name, metric_name, value):

    metrics.append({

        "Model": model_name,

        "Metric": metric_name,

        "Value": round(float(value),4)

    })


# ==========================================================
# Popularity Prediction
# ==========================================================

print("\nTraining Popularity Model...")

y = df["popularity"]

X_train,X_test,y_train,y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42

)

popularity_model = RandomForestRegressor(

    n_estimators=200,

    random_state=42

)

popularity_model.fit(

    X_train,

    y_train

)

pred = popularity_model.predict(X_test)

mae = mean_absolute_error(y_test,pred)

rmse = mean_squared_error(y_test,pred)**0.5

r2 = r2_score(y_test,pred)

save_metrics("Popularity","MAE",mae)

save_metrics("Popularity","RMSE",rmse)

save_metrics("Popularity","R2",r2)

joblib.dump(

    popularity_model,

    f"{MODEL_DIR}/popularity_model.pkl"

)

print("✓ Popularity Model Saved")

# ==========================================================
# Trending Prediction
# ==========================================================

print("\nTraining Trending Model...")

y = df["trending_label"]

X_train,X_test,y_train,y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42

)

trending_model = RandomForestClassifier(

    n_estimators=200,

    random_state=42

)

trending_model.fit(

    X_train,

    y_train

)

pred = trending_model.predict(X_test)

acc = accuracy_score(y_test,pred)

save_metrics(

    "Trending",

    "Accuracy",

    acc

)

joblib.dump(

    trending_model,

    f"{MODEL_DIR}/trending_model.pkl"

)

print("✓ Trending Model Saved")

# ==========================================================
# Top10 Prediction
# ==========================================================

print("\nTraining Top10 Model...")

y = df["top10_label"]

X_train,X_test,y_train,y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42

)

top10_model = RandomForestClassifier(

    n_estimators=200,

    random_state=42

)

top10_model.fit(

    X_train,

    y_train

)

pred = top10_model.predict(X_test)

acc = accuracy_score(y_test,pred)

save_metrics(

    "Top10",

    "Accuracy",

    acc

)

joblib.dump(

    top10_model,

    f"{MODEL_DIR}/top10_model.pkl"

)

print("✓ Top10 Model Saved")

# ==========================================================
# Artist Success Prediction
# ==========================================================

print("\nTraining Artist Success Model...")

y = df["artist_success_score"]

X_train,X_test,y_train,y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42

)

artist_model = RandomForestRegressor(

    n_estimators=200,

    random_state=42

)

artist_model.fit(

    X_train,

    y_train

)

pred = artist_model.predict(X_test)

mae = mean_absolute_error(y_test,pred)

rmse = mean_squared_error(y_test,pred)**0.5

r2 = r2_score(y_test,pred)

save_metrics(

    "Artist Success",

    "MAE",

    mae

)

save_metrics(

    "Artist Success",

    "RMSE",

    rmse

)

save_metrics(

    "Artist Success",

    "R2",

    r2

)

joblib.dump(

    artist_model,

    f"{MODEL_DIR}/artist_success_model.pkl"

)

print("✓ Artist Success Model Saved")

# ==========================================================
# Save Metrics
# ==========================================================

metrics_df = pd.DataFrame(metrics)

metrics_df.to_csv(

    "models/model_metrics.csv",

    index=False

)

print("\nModel Metrics Saved")

# ==========================================================
# Feature Importance
# ==========================================================

importance = pd.DataFrame({

    "Feature":FEATURES,

    "Importance":popularity_model.feature_importances_

})

importance.to_csv(

    "models/feature_importance.csv",

    index=False

)

print("Feature Importance Saved")

print("\n" + "="*60)

print("All Models Trained Successfully")

print("="*60)