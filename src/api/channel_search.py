from src.api.youtube_client import get_youtube_service


def search_creators(keyword, max_results=10):
    youtube = get_youtube_service()

    response = youtube.search().list(
        part="snippet",
        q=keyword,
        type="channel",
        maxResults=max_results
    ).execute()

    channel_ids = [
        item["id"]["channelId"]
        for item in response.get("items", [])
    ]

    if not channel_ids:
        return []

    channel_response = youtube.channels().list(
        part="snippet,statistics",
        id=",".join(channel_ids)
    ).execute()

    creators = []

    for channel in channel_response.get("items", []):
        stats = channel.get("statistics", {})
        snippet = channel.get("snippet", {})

        creators.append({
            "channel_id": channel["id"],
            "channel_name": snippet.get("title", "Unknown"),
            "description": snippet.get("description", ""),
            "country": snippet.get("country", "Not available"),
            "published_at": snippet.get("publishedAt", ""),
            "subscribers": int(stats.get("subscriberCount", 0)),
            "total_views": int(stats.get("viewCount", 0)),
            "total_videos": int(stats.get("videoCount", 0)),
            "hidden_subscribers": stats.get(
                "hiddenSubscriberCount", False
            )
        })

    return creators


def get_channel_video_metrics(channel_id, max_videos=10):
    """Analyze up to 10 most-viewed public videos of a channel."""
    youtube = get_youtube_service()

    search_response = youtube.search().list(
        part="id",
        channelId=channel_id,
        type="video",
        order="viewCount",
        maxResults=max_videos
    ).execute()

    video_ids = [
        item["id"]["videoId"]
        for item in search_response.get("items", [])
    ]

    if not video_ids:
        return {
            "sample_videos": 0,
            "sample_views": 0,
            "sample_likes": 0,
            "videos_with_visible_likes": 0
        }

    video_response = youtube.videos().list(
        part="statistics",
        id=",".join(video_ids)
    ).execute()

    sample_views = 0
    sample_likes = 0
    visible_likes = 0

    for video in video_response.get("items", []):
        stats = video.get("statistics", {})

        sample_views += int(stats.get("viewCount", 0))

        if "likeCount" in stats:
            sample_likes += int(stats["likeCount"])
            visible_likes += 1

    return {
        "sample_videos": len(video_response.get("items", [])),
        "sample_views": sample_views,
        "sample_likes": sample_likes,
        "videos_with_visible_likes": visible_likes
    }
