import streamlit as st
import pandas as pd
import os


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="About K-Wave Analytics",
    page_icon="📄",
    layout="wide"
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
    margin-bottom:20px;
}

.card{
    background:#1E1E1E;
    border-radius:15px;
    padding:20px;
    border:1px solid #333;
    height:100%;
}

.metric-card{
    background:#262730;
    border-radius:15px;
    padding:20px;
    border:1px solid #404040;
    text-align:center;
}

.metric-title{
    color:#BBBBBB;
    font-size:16px;
}

.metric-value{
    color:white;
    font-size:30px;
    font-weight:bold;
}

.team-card{
    background:#1E1E1E;
    border-radius:18px;
    padding:25px;
    border:1px solid #333;
    min-height:350px;
}

.team-name{
    color:white;
    font-size:26px;
    font-weight:bold;
}

.team-role{
    color:#BBBBBB;
    font-size:18px;
    margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# HERO
# ==========================================================

st.markdown("""

<div class="hero">

<h1>🎵 K-Wave Analytics</h1>

<h3>AI-Powered K-Pop Trend Intelligence Platform</h3>

<p>

Analyze Songs • Predict Popularity • Detect Trends •
Recommend Music using Machine Learning

</p>

</div>

""", unsafe_allow_html=True)


# ==========================================================
# PROJECT OVERVIEW
# ==========================================================

st.subheader("📌 Project Overview")

st.write("""

K-Wave Analytics is an intelligent K-Pop music analytics platform
built using Machine Learning and Streamlit.

The system analyzes songs, predicts popularity, identifies
trending songs, recommends similar music, evaluates artist
performance and provides interactive visual dashboards.

It combines Data Science, Machine Learning, Visualization,
Recommendation Systems and Business Intelligence into one
modern web application.

""")


st.divider()


# ==========================================================
# PROJECT FEATURES
# ==========================================================

st.subheader("✨ Core Features")

c1, c2, c3 = st.columns(3)

with c1:

    st.success("🎵 Song Analytics")
    st.success("📊 Interactive Dashboard")
    st.success("⭐ Popularity Prediction")
    st.success("🔥 Trending Detection")


with c2:

    st.success("🏆 Top 10 Prediction")
    st.success("👑 Artist Success Score")
    st.success("🎧 Music Recommendation")
    st.success("📈 Trend Visualization")


with c3:

    st.success("📥 CSV Export")
    st.success("🤖 Machine Learning")
    st.success("⚡ Real-time Prediction")
    st.success("📉 Business Insights")


st.divider()


# ==========================================================
# TECHNOLOGY STACK
# ==========================================================

st.subheader("🛠 Technology Stack")

tech = pd.DataFrame({

    "Technology":[
        "Python",
        "Streamlit",
        "Pandas",
        "NumPy",
        "Scikit-Learn",
        "Plotly",
        "Joblib"
    ],

    "Purpose":[
        "Programming Language",
        "Interactive Dashboard",
        "Data Processing",
        "Numerical Computing",
        "Machine Learning",
        "Visualization",
        "Model Serialization"
    ]

})

st.dataframe(
    tech,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ==========================================================
# MACHINE LEARNING MODELS
# ==========================================================

st.subheader("🤖 Machine Learning Models")

models = pd.DataFrame({

    "Prediction":[
        "Popularity Score",
        "Trending Song",
        "Top 10 Song",
        "Artist Success"
    ],

    "Algorithm":[
        "Random Forest Regressor",
        "Random Forest Classifier",
        "Random Forest Classifier",
        "Random Forest Regressor"
    ]

})

st.dataframe(
    models,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ==========================================================
# DATASET STATISTICS
# ==========================================================

st.subheader("📊 Dataset Statistics")

try:

    df = pd.read_csv("data/ml_dataset.csv")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Songs",
            len(df)
        )

    with c2:

        st.metric(
            "Artists",
            df["artist"].nunique()
        )

    with c3:

        st.metric(
            "Album Types",
            df["album_type"].nunique()
        )

    with c4:

        st.metric(
            "Average Popularity",
            round(df["popularity"].mean(), 2)
        )

except FileNotFoundError:

    st.warning("Dataset not found.")


# ==========================================================
# PROJECT WORKFLOW
# ==========================================================

st.subheader("🔄 Project Workflow")

workflow1, workflow2, workflow3, workflow4, workflow5, workflow6 = st.columns(6)

with workflow1:
    st.info("📂 Dataset")

with workflow2:
    st.info("🧹 Cleaning")

with workflow3:
    st.info("⚙ Feature Engineering")

with workflow4:
    st.info("🤖 ML Training")

with workflow5:
    st.info("🎯 Prediction")

with workflow6:
    st.info("📊 Dashboard")


st.divider()


# ==========================================================
# PROJECT STRUCTURE
# ==========================================================

st.subheader("📁 Project Structure")

structure = """
K_Wave_Analytics/

│
├── dashboard/
│   ├── Home.py
│   └── pages/
│       ├── 1_Analytics.py
│       ├── 2_AI_Predictions.py
│       ├── 3_Recommendation.py
│       └── 4_About.py
│
├── src/
│   ├── data_preprocessing.py
│   ├── feature_engineering.py
│   ├── train_models.py
│   ├── predict.py
│   ├── recommendation.py
│   ├── charts.py
│   └── utils.py
│
├── models/
│
├── data/
│
├── assets/
│
└── requirements.txt
"""

st.code(structure)


st.divider()


# ==========================================================
# PROJECT FEATURES
# ==========================================================

st.subheader("🚀 Major Functionalities")

left, right = st.columns(2)

with left:

    st.success("✔ Interactive Dashboard")
    st.success("✔ AI Prediction")
    st.success("✔ Recommendation Engine")
    st.success("✔ Trend Analysis")
    st.success("✔ Artist Analytics")
    st.success("✔ Song Search")


with right:

    st.success("✔ Machine Learning Models")
    st.success("✔ Plotly Visualizations")
    st.success("✔ CSV Export")
    st.success("✔ Feature Engineering")
    st.success("✔ Dataset Insights")
    st.success("✔ User Friendly Interface")


st.divider()


# ==========================================================
# PROJECT TEAM
# ==========================================================

st.subheader("👥 Project Team")

col1, col2 = st.columns(2)


# ==========================================================
# HETVI
# ==========================================================

with col1:

    st.markdown("""
    <div class="team-card">

    <div class="team-name">
    👩‍💻 Lashkari Hetvi
    </div>

    <div class="team-role">
    AI / Machine Learning Developer
    </div>

    <hr>

    <h4>Responsibilities</h4>

    <ul>
        <li>Data Processing & Cleaning</li>
        <li>Feature Engineering</li>
        <li>Machine Learning Model Development</li>
        <li>Model Training & Evaluation</li>
        <li>Popularity Prediction</li>
        <li>Trending Prediction</li>
        <li>Top 10 Prediction</li>
        <li>Artist Success Prediction</li>
    </ul>

    <h4>Technologies</h4>

    <p>
    Python • Pandas • NumPy • Scikit-Learn •
    Machine Learning
    </p>

    </div>
    """, unsafe_allow_html=True)


# ==========================================================
# KRISHNA
# ==========================================================

with col2:

    st.markdown("""
    <div class="team-card">

    <div class="team-name">
    🎨 Tank Krishna
    </div>

    <div class="team-role">
    UI / Dashboard Designer
    </div>

    <hr>

    <h4>Responsibilities</h4>

    <ul>
        <li>Dashboard UI Design</li>
        <li>Streamlit Interface Development</li>
        <li>Page Layout & Navigation</li>
        <li>Interactive Components</li>
        <li>Charts & Visual Presentation</li>
        <li>User Experience Design</li>
        <li>Recommendation Page UI</li>
        <li>Analytics Dashboard UI</li>
    </ul>

    <h4>Technologies</h4>

    <p>
    Streamlit • Plotly • HTML • CSS •
    Data Visualization
    </p>

    </div>
    """, unsafe_allow_html=True)


st.divider()


# ==========================================================
# VERSION INFORMATION
# ==========================================================

st.subheader("📦 Version Information")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Version",
        "1.0"
    )

with c2:

    st.metric(
        "ML Models",
        "4"
    )

with c3:

    st.metric(
        "Framework",
        "Streamlit"
    )

with c4:

    st.metric(
        "Language",
        "Python"
    )


st.divider()



# ==========================================================
# PROJECT SUMMARY
# ==========================================================

st.subheader("📄 Project Summary")

summary = pd.DataFrame({

    "Module":[
        "Dashboard",
        "Analytics",
        "Prediction",
        "Recommendation",
        "Visualization",
        "Machine Learning"
    ],

    "Status":[
        "Completed ✅",
        "Completed ✅",
        "Completed ✅",
        "Completed ✅",
        "Completed ✅",
        "Completed ✅"
    ]

})

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)


st.divider()



# ==========================================================
# THANK YOU
# ==========================================================

st.markdown(
"""
<div style="background:linear-gradient(135deg,#6C63FF,#8E44AD);
padding:30px;
border-radius:20px;
text-align:center;
color:white;">

<h2>💜 Thank You for Visiting K-Wave Analytics</h2>

<p>
An AI-Powered K-Pop Trend Intelligence Platform
developed using Machine Learning and Streamlit.
</p>

<p>
Predict • Analyze • Recommend • Discover
</p>

</div>
""",
unsafe_allow_html=True
)


st.divider()


# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
"""
<center>

<h2>🎵 K-Wave Analytics</h2>

<p>
AI-Powered K-Pop Trend Intelligence Platform
</p>

<p>
Built with ❤️ using
Python • Streamlit • Pandas • Plotly • Scikit-Learn
</p>

<hr>

<p>
© 2026 Lashkari Hetvi & Tank Krishna | All Rights Reserved
</p>

</center>
""",
unsafe_allow_html=True
)