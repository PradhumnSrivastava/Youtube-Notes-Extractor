# Import the YouTubeTranscriptApi library
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import RequestBlocked, NoTranscriptFound


# ---------------------------------------------------------
# FUNCTION: get_video_id
# ---------------------------------------------------------
# Extract the YouTube video ID from different URL formats

def get_video_id(url):

    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]

    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]

    else:
        raise ValueError("Invalid YouTube URL")


# ---------------------------------------------------------
# FUNCTION: get_transcript
# ---------------------------------------------------------
# Retrieve transcript subtitles with timestamps

def get_transcript(url):

    video_id = get_video_id(url)

    try:

        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=["en", "hi"]
        )

    except RequestBlocked:
        print("YouTube blocked the request.")
        return []

    except NoTranscriptFound:
        print("No transcript available for this video.")
        return []

    except Exception as e:
        print("Transcript error:", e)
        return []

    segments = []

    for item in transcript:

        segments.append({
            "text": item["text"],
            "start": round(item["start"], 2)
        })

    return segments