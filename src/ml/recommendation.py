
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def normalize_scores(values):
    """Convert values into a 0-100 scale."""
    values = pd.Series(values, dtype=float).fillna(0)

    maximum = values.max()

    if maximum <= 0:
        return pd.Series(0.0, index=values.index)

    return (values / maximum) * 100


def calculate_brand_relevance(creators, brand_keyword):
    """Compare brand keyword with creator names and descriptions."""

    descriptions = []

    for creator in creators:
        text = " ".join([
            str(creator.get("channel_name", "")),
            str(creator.get("description", ""))
        ])
        descriptions.append(text)

    documents = [brand_keyword] + descriptions

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    try:
        matrix = vectorizer.fit_transform(documents)

        similarities = cosine_similarity(
            matrix[0:1],
            matrix[1:]
        )[0]

        return similarities * 100

    except ValueError:
        return np.zeros(len(creators))


def recommend_creators(
    creators,
    brand_keyword,
    engagement_data=None
):
    """Rank creators using a provisional suitability score."""

    if not creators:
        return pd.DataFrame()

    if not brand_keyword or not brand_keyword.strip():
        raise ValueError("Please enter a brand or product keyword.")

    engagement_data = engagement_data or {}

    brand_scores = calculate_brand_relevance(
        creators,
        brand_keyword.strip()
    )

    results = []

    for index, creator in enumerate(creators):
        channel_id = creator["channel_id"]

        videos = engagement_data.get(channel_id)

        engagement_rate = 0.0

        if videos is not None and not videos.empty:
            if "engagement_rate" in videos.columns:
                engagement_rate = float(
                    videos["engagement_rate"].mean()
                )

        results.append({
            "Channel": creator.get("channel_name", "Unknown"),
            "Channel ID": channel_id,
            "Subscribers": int(creator.get("subscribers", 0)),
            "Total Views": int(creator.get("total_views", 0)),
            "Total Videos": int(creator.get("total_videos", 0)),
            "Engagement Rate": engagement_rate,
            "Brand Relevance": float(brand_scores[index])
        })

    df = pd.DataFrame(results)

    df["Reach Score"] = normalize_scores(
        np.log1p(df["Subscribers"])
    )

    df["Engagement Score"] = normalize_scores(
        df["Engagement Rate"]
    )

    df["Activity Score"] = normalize_scores(
        np.log1p(df["Total Videos"])
    )

    df["Suitability Score"] = (
        df["Reach Score"] * 0.25
        + df["Engagement Score"] * 0.30
        + df["Brand Relevance"] * 0.35
        + df["Activity Score"] * 0.10
    )

    df["Suitability Score"] = df["Suitability Score"].round(2)

    df = df.sort_values(
        "Suitability Score",
        ascending=False
    ).reset_index(drop=True)

    df.insert(0, "Rank", range(1, len(df) + 1))

    return df
