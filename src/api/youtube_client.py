from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import YOUTUBE_API_KEY


def get_youtube_service():
    if not YOUTUBE_API_KEY:
        raise ValueError(
            "YouTube API key missing. Check your .env file."
        )

    return build(
        "youtube",
        "v3",
        developerKey=YOUTUBE_API_KEY,
        cache_discovery=False
    )


def test_connection():
    try:
        youtube = get_youtube_service()

        response = youtube.videos().list(
            part="snippet",
            chart="mostPopular",
            regionCode="US",
            maxResults=1
        ).execute()

        videos = response.get("items", [])

        if videos:
            return {
                "success": True,
                "message": "YouTube API connected successfully!",
                "video_title": videos[0]["snippet"]["title"]
            }

        return {
            "success": True,
            "message": "API connected, but no videos returned."
        }

    except HttpError as error:
        return {
            "success": False,
            "message": f"YouTube API error: {error}"
        }

    except Exception as error:
        return {
            "success": False,
            "message": str(error)
        }


if __name__ == "__main__":
    result = test_connection()

    if result["success"]:
        print(result["message"])
        if "video_title" in result:
            print("Sample video:", result["video_title"])
    else:
        print("Connection failed:", result["message"])
