# ==========================================
# IMDb Movie Analysis Project
# ==========================================

"""
Title: IMDb Movie Analysis

Problem Statement:
Many movies are released every year with different budgets, genres,
directors, and IMDb ratings. It is difficult to manually analyze large
movie datasets and identify patterns such as:
- Which genre has higher IMDb ratings?
- Whether high-budget movies get better ratings?
- Distribution of movie budgets?
- Relationship between budget and IMDb score?

This project analyzes movie data using Python and visualization libraries.
"""

# ==========================================
# Import Libraries
# ==========================================

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns

# ==========================================
# Project Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "movies.csv"
IMAGE_DIR = BASE_DIR / "images"

IMAGE_DIR.mkdir(exist_ok=True)

# ==========================================
# Load Dataset
# ==========================================


def load_data():
    print("Loading dataset...")

    df = pd.read_csv(DATA_FILE, encoding="latin1")

    print("Dataset Loaded Successfully!\n")

    return df


# ==========================================
# Clean Dataset
# ==========================================


def clean_data(df):
    df = df[['Movie', 'Genre', 'Budget', 'IMDb score']]

    df = df.dropna()

    df['Budget'] = pd.to_numeric(df['Budget'], errors='coerce')
    df['IMDb score'] = pd.to_numeric(df['IMDb score'], errors='coerce')

    df = df.dropna()

    df = df[df['Budget'] > 0]

    return df


# ==========================================
# Analyze Dataset
# ==========================================


def analyze_data(df):

    print("First 5 Rows:\n")
    print(df.head())

    print("\nColumns in Dataset:\n")
    print(df.columns)

    print("\nDataset Shape:")
    print(df.shape)

    print("\nBasic Statistics:")
    print(df.describe())

    correlation = df[['Budget', 'IMDb score']].corr()

    print("\nCorrelation Matrix:")
    print(correlation)

    genre_rating = (
        df.groupby("Genre")["IMDb score"]
        .mean()
        .sort_values(ascending=False)
    )

    return correlation, genre_rating


# ==========================================
# Visualizations
# ==========================================


def visualize_data(df, correlation, genre_rating):

    sns.set_style("darkgrid")

    # Scatter Plot
    plt.figure(figsize=(12, 6))

    sns.scatterplot(
        data=df,
        x="Budget",
        y="IMDb score",
        hue="Genre"
    )

    plt.title("Budget vs IMDb Rating")
    plt.xlabel("Budget")
    plt.ylabel("IMDb Rating")
    plt.xticks(rotation=45)

    plt.savefig(IMAGE_DIR / "budget_vs_rating.png")
    plt.show()

    # Genre Rating

    plt.figure(figsize=(12, 6))

    genre_rating.plot(kind="bar")

    plt.title("Average IMDb Rating by Genre")
    plt.xlabel("Genre")
    plt.ylabel("Average IMDb Rating")

    plt.xticks(rotation=45)

    plt.savefig(IMAGE_DIR / "genre_rating.png")
    plt.show()

    # Budget Distribution

    plt.figure(figsize=(10, 6))

    sns.histplot(df["Budget"], bins=30)

    plt.title("Movie Budget Distribution")
    plt.xlabel("Budget")

    plt.savefig(IMAGE_DIR / "budget_distribution.png")
    plt.show()

    # Heatmap

    plt.figure(figsize=(5, 4))

    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm"
    )

    plt.title("Correlation Heatmap")

    plt.savefig(IMAGE_DIR / "correlation_heatmap.png")
    plt.show()

    # Interactive Plot

    fig = px.scatter(
        df,
        x="Budget",
        y="IMDb score",
        color="Genre",
        hover_data=["Movie"],
        title="Interactive Budget vs IMDb Rating"
    )

    fig.write_html(IMAGE_DIR / "interactive_budget_vs_rating.html")

    fig.show()


# ==========================================
# Insights
# ==========================================


def generate_insights(df, correlation, genre_rating):

    print("\nPROJECT INSIGHTS\n")

    highest_rated_genre = genre_rating.idxmax()

    print(f"Highest Rated Genre: {highest_rated_genre}")

    if correlation.iloc[0, 1] > 0.3:
        print("Higher budget movies generally receive higher IMDb ratings.")
    elif correlation.iloc[0, 1] > 0:
        print("There is only a weak positive relationship between budget and IMDb ratings.")
    else:
        print("Movie budget has little or no effect on IMDb ratings.")

    print("\nTop 10 Highest Rated Movies:\n")

    top_movies = df.sort_values(
        by="IMDb score",
        ascending=False
    )

    print(top_movies[["Movie", "Genre", "IMDb score"]].head(10))

    print("\nTop 10 Highest Budget Movies:\n")

    high_budget = df.sort_values(
        by="Budget",
        ascending=False
    )

    print(high_budget[["Movie", "Budget"]].head(10))

    print("\nProject Completed Successfully!")


# ==========================================
# Main Function
# ==========================================


def main():

    df = load_data()

    df = clean_data(df)

    correlation, genre_rating = analyze_data(df)

    visualize_data(df, correlation, genre_rating)

    generate_insights(df, correlation, genre_rating)


# ==========================================
# Run Program
# ==========================================

if __name__ == "__main__":
    main()