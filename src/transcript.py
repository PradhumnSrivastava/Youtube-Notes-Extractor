# Import the YouTubeTranscriptApi library
# This library allows us to fetch subtitles (transcripts) from YouTube videos
from youtube_transcript_api import YouTubeTranscriptApi


# ---------------------------------------------------------
# FUNCTION: get_video_id
# ---------------------------------------------------------
# This function extracts the YouTube video ID from a URL.
# YouTube URLs can appear in different formats, so we check
# for the common patterns and extract the ID accordingly.

def get_video_id(url):

    # Case 1: Standard YouTube URL
    # Example: https://www.youtube.com/watch?v=abc123
    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]

    # Case 2: Shortened YouTube URL
    # Example: https://youtu.be/abc123
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]

    # If the URL format is not recognized, raise an error
    else:
        raise ValueError("Invalid YouTube URL")


# ---------------------------------------------------------
# FUNCTION: get_transcript
# ---------------------------------------------------------
# This function retrieves the transcript (subtitles) of a YouTube video.
# It also extracts timestamps for each subtitle segment.

def get_transcript(url):

    # Extract the video ID from the provided URL
    video_id = get_video_id(url)

    # Create an instance of the YouTube Transcript API
    api = YouTubeTranscriptApi()

    # Fetch the transcript for the video
    # We try English first, then Hindi if English is unavailable
    transcript = api.fetch(video_id, languages=["en", "hi"])

    # This list will store the processed transcript segments
    segments = []

    # Loop through each subtitle segment returned by the API
    for item in transcript:

        # Each item contains text and start time
        # We store them in a dictionary format
        segments.append({
            "text": item.text,                 # Subtitle text
            "start": round(item.start, 2)      # Timestamp rounded to 2 decimal places
        })

    # Return the list of transcript segments
    # Example output:
    # [
    #   {"text": "Welcome to Python tutorial", "start": 0.42},
    #   {"text": "Today we will learn variables", "start": 3.12}
    # ]
    return segments