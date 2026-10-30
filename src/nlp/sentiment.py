import pandas as pd
from textblob import TextBlob
from googleapiclient.errors import HttpError

from src.api.youtube_client import get_youtube_service


def get_video_comments(video_id, max_comments=100):
    youtube = get_youtube_service()

    try:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=min(max_comments, 100),
            textFormat="plainText"
        ).execute()

    except HttpError as error:
        raise ValueError(
            "Comments unavailable. They may be disabled for this video "
            "or the API request may have failed."
        ) from error

    records = []

    for item in response.get("items", []):
        comment = item["snippet"]["topLevelComment"]["snippet"]

        records.append({
            "author": comment.get("authorDisplayName", "Unknown"),
            "comment": comment.get("textDisplay", ""),
            "like_count": int(comment.get("likeCount", 0)),
            "published_at": comment.get("publishedAt", "")
        })

    return pd.DataFrame(records)


def analyze_comment_sentiment(comments):
    if comments.empty:
        return pd.DataFrame()

    results = comments.copy()

    results["sentiment_score"] = results["comment"].apply(
        lambda text: float(TextBlob(str(text)).sentiment.polarity)
    )

    def classify_sentiment(score):
        if score > 0.05:
            return "Positive"
        elif score < -0.05:
            return "Negative"
        return "Neutral"

    results["sentiment"] = results["sentiment_score"].apply(
        classify_sentiment
    )

    return results


def get_sentiment_summary(analyzed_comments):
    if analyzed_comments.empty:
        return {}

    counts = analyzed_comments["sentiment"].value_counts()

    total = len(analyzed_comments)

    return {
        "total_comments": total,
        "positive": int(counts.get("Positive", 0)),
        "negative": int(counts.get("Negative", 0)),
        "neutral": int(counts.get("Neutral", 0)),
        "average_sentiment_score": float(
            round(analyzed_comments["sentiment_score"].mean(), 3)
        ),
        "positive_percentage": round(
            counts.get("Positive", 0) / total * 100, 2
        )
    }
