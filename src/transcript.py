from youtube_transcript_api import YouTubeTranscriptApi


def get_video_id(url):

    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]

    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]

    else:
        raise ValueError("Invalid YouTube URL")


def get_transcript(url):

    video_id = get_video_id(url)

    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id, languages=["en", "hi"])

    segments = []

    for item in transcript:
        segments.append({
            "text": item.text,
            "start": round(item.start, 2)
        })

    return segments