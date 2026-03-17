# Import the YouTubeTranscriptApi library
# This library allows us to fetch subtitles (transcripts) from YouTube videos
from youtube_transcript_api import YouTubeTranscriptApi


# ---------------------------------------------------------
# FUNCTION: get_video_id
# ---------------------------------------------------------
# Extracts the YouTube video ID from different URL formats.

def get_video_id(url):

    # Case 1: Standard YouTube URL
    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]

    # Case 2: Short YouTube URL
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]

    else:
        raise ValueError("Invalid YouTube URL")


# ---------------------------------------------------------
# FUNCTION: get_transcript
# ---------------------------------------------------------
# Retrieves transcript subtitles with timestamps.
# Handles cases where transcripts are unavailable or blocked.

def get_transcript(url):

    video_id = get_video_id(url)

    try:

        # Fetch transcript using the stable static method
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=["en", "hi"]
        )

    except Exception as e:

        # If transcript cannot be retrieved
        print("Transcript fetch error:", e)
        return []


    segments = []

    # Convert transcript objects into simple dictionary format
    for item in transcript:

        segments.append({
            "text": item["text"],
            "start": round(item["start"], 2)
        })

    return segments