from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

# ======================================================
# Page Configuration
# ======================================================

st.set_page_config(
    page_title="IMDb Movie Analysis Dashboard",
    page_icon="🎬",
    layout="wide"
)

# ======================================================
# Load Dataset
# ======================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "movies.csv"


@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE, encoding="latin1")


df = load_data()

# ======================================================
# Sidebar
# ======================================================

st.sidebar.title("🎛 Dashboard Filters")

genres = sorted(df["Genre"].dropna().unique())

selected_genre = st.sidebar.selectbox(
    "Genre",
    ["All"] + genres
)

years = sorted(df["Release year"].dropna().unique())

selected_year = st.sidebar.selectbox(
    "Release Year",
    ["All"] + list(years)
)

min_rating = st.sidebar.slider(
    "Minimum IMDb Rating",
    min_value=1.0,
    max_value=10.0,
    value=1.0,
    step=0.1
)

# ======================================================
# Apply Filters
# ======================================================

filtered_df = df.copy()

if selected_genre != "All":
    filtered_df = filtered_df[
        filtered_df["Genre"] == selected_genre
    ]

if selected_year != "All":
    filtered_df = filtered_df[
        filtered_df["Release year"] == selected_year
    ]

filtered_df = filtered_df[
    filtered_df["IMDb score"] >= min_rating
]

# ======================================================
# Search Movie
# ======================================================

search_movie = st.text_input(
    "🔍 Search Movie",
    placeholder="Type a movie name..."
)

if search_movie:
    filtered_df = filtered_df[
        filtered_df["Movie"].str.contains(
            search_movie,
            case=False,
            na=False
        )
    ]


# ======================================================
# Title
# ======================================================

st.title("🎬 IMDb Movie Analysis Dashboard")

st.write(
    "Analyze IMDb movie data using interactive charts and filters."
)

# ======================================================
# KPI Cards
# ======================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🎥 Movies",
        filtered_df.shape[0]
    )

with col2:
    st.metric(
        "📄 Columns",
        filtered_df.shape[1]
    )

with col3:
    st.metric(
        "⭐ Avg IMDb Rating",
        round(filtered_df["IMDb score"].mean(), 2)
    )

with col4:
    st.metric(
        "💰 Avg Budget",
        f"${filtered_df['Budget'].mean()/1_000_000:.1f}M"
    )

st.divider()

# ======================================================
# Dataset Preview
# ======================================================

st.subheader("📋 Dataset Preview")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)

st.write(f"Movies Available : **{filtered_df.shape[0]}**")
st.write(f"Columns : **{filtered_df.shape[1]}**")

st.divider()

# ======================================================
# Average IMDb Rating by Genre
# ======================================================

# ==========================================
# Charts Row 1
# ==========================================

col_left, col_right = st.columns(2)

with col_left:

    st.subheader("🎭 Average IMDb Rating by Genre")

    genre_rating = (
        filtered_df
        .groupby("Genre")["IMDb score"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        genre_rating,
        x="Genre",
        y="IMDb score",
        color="IMDb score",
        title="Average IMDb Rating"
    )

    st.plotly_chart(fig, use_container_width=True)

with col_right:

    st.subheader("📈 Budget vs IMDb Rating")

    fig2 = px.scatter(
        filtered_df,
        x="Budget",
        y="IMDb score",
        color="Genre",
        hover_data=["Movie"]
    )

    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ======================================================
# Charts Row 2
# ======================================================

col_left, col_right = st.columns(2)

# ------------------------------------------
# Budget Distribution
# ------------------------------------------

with col_left:

    st.subheader("💰 Budget Distribution")

    fig3 = px.histogram(
        filtered_df,
        x="Budget",
        nbins=30,
        title="Movie Budget Distribution"
    )

    st.plotly_chart(fig3, use_container_width=True)

# ------------------------------------------
# Genre Distribution
# ------------------------------------------

with col_right:

    st.subheader("🥧 Genre Distribution")

    genre_count = (
        filtered_df["Genre"]
        .value_counts()
        .reset_index()
    )

    genre_count.columns = ["Genre", "Movies"]

    fig4 = px.pie(
        genre_count,
        names="Genre",
        values="Movies",
        hole=0.4,
        title="Movies by Genre"
    )

    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ======================================================
# Top Rated Movies
# ======================================================

st.subheader("🏆 Top 10 Highest Rated Movies")

top_movies = (
    filtered_df[
        ["Movie", "Genre", "IMDb score"]
    ]
    .sort_values(
        by="IMDb score",
        ascending=False
    )
    .head(10)
)

st.dataframe(top_movies)

st.divider()

# ======================================================
# Top 10 Highest Budget Movies
# ======================================================

st.subheader("💰 Top 10 Highest Budget Movies")

top_budget = (
    filtered_df[
        ["Movie", "Budget"]
    ]
    .sort_values(
        by="Budget",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_budget,
    use_container_width=True
)

st.divider()

# ======================================================
# Project Insights
# ======================================================

st.subheader("📌 Project Insights")

# Highest Rated Genre
highest_genre = (
    filtered_df
    .groupby("Genre")["IMDb score"]
    .mean()
    .idxmax()
)

st.success(f"⭐ Highest Rated Genre: {highest_genre}")

# Correlation
correlation = filtered_df[
    ["Budget", "IMDb score"]
].corr().iloc[0, 1]

st.info(
    f"📊 Correlation between Budget and IMDb Rating: {correlation:.2f}"
)

# Interpretation
if correlation > 0.3:
    st.success(
        "Higher-budget movies generally receive better IMDb ratings."
    )
elif correlation > 0:
    st.warning(
        "There is only a weak relationship between budget and IMDb rating."
    )
else:
    st.error(
        "Movie budget has little or no relationship with IMDb rating."
    )

st.divider()


# ======================================================
# Download CSV
# ======================================================

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Filtered Dataset",
    data=csv,
    file_name="filtered_movies.csv",
    mime="text/csv"
)

st.divider()

# ======================================================
# Footer
# ======================================================

st.markdown("---")

st.markdown(
"""
## 👩‍💻 Developed By

**Uthsavi C U**

B.Tech Artificial Intelligence & Data Science

### 🛠 Technologies Used

- Python
- Pandas
- Plotly
- Streamlit

### 📊 Features

- Interactive Dashboard
- Movie Search
- Genre & Year Filters
- Budget Analysis
- IMDb Rating Analysis
- Download Filtered Dataset
"""
)