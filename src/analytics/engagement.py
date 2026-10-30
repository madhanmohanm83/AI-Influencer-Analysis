import pandas as pd

from src.api.youtube_client import get_youtube_service


def get_recent_video_engagement(channel_id, max_videos=10):
    youtube = get_youtube_service()

    # Step 1: Get channel uploads playlist
    channel_response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()

    channels = channel_response.get("items", [])

    if not channels:
        return pd.DataFrame()

    uploads_playlist = channels[0][
        "contentDetails"
    ]["relatedPlaylists"]["uploads"]

    # Step 2: Get recent videos
    playlist_response = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=uploads_playlist,
        maxResults=min(max_videos, 50)
    ).execute()

    video_ids = [
        item["contentDetails"]["videoId"]
        for item in playlist_response.get("items", [])
    ]

    if not video_ids:
        return pd.DataFrame()

    # Step 3: Get video statistics
    video_response = youtube.videos().list(
        part="snippet,statistics",
        id=",".join(video_ids)
    ).execute()

    records = []

    for video in video_response.get("items", []):
        stats = video.get("statistics", {})
        snippet = video.get("snippet", {})

        views = int(stats.get("viewCount", 0))

        likes = (
            int(stats["likeCount"])
            if "likeCount" in stats else None
        )

        comments = (
            int(stats["commentCount"])
            if "commentCount" in stats else None
        )

        if views > 0 and likes is not None and comments is not None:
            engagement_rate = (
                (likes + comments) / views
            ) * 100
        else:
            engagement_rate = None

        records.append({
            "video_id": video["id"],
            "video_title": snippet.get("title", ""),
            "published_at": snippet.get("publishedAt", ""),
            "views": views,
            "likes": likes,
            "comments": comments,
            "engagement_rate": engagement_rate
        })

    return pd.DataFrame(records)


def get_engagement_summary(videos):
    if videos.empty:
        return {}

    valid_rates = videos["engagement_rate"].dropna()

    return {
        "total_videos": len(videos),
        "total_views": int(videos["views"].sum()),
        "total_likes": int(videos["likes"].sum()),
        "total_comments": int(videos["comments"].sum()),
        "average_engagement_rate": (
            round(valid_rates.mean(), 2)
            if not valid_rates.empty else None
        )
    }
