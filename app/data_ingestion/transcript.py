from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from googleapiclient.discovery import build
from app.core.config import settings
from app.utils.helpers import log_exception
import re

def extract_video_id(url):
    """Extracts the YouTube video ID from a URL."""
    try:
        # Check for shortened URL first
        match = re.search(r"youtu\.be/([a-zA-Z0-9_-]+)", url)
        if match:
            return match.group(1)

        # Then check for standard URL
        match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
        if match:
            return match.group(1)

        return None  # Return None if no ID is found
    except Exception as e:
        print(f"Error extracting video ID: {e}")
        return None


def get_video_language(video_id):
    """
    Retrieves the language of a YouTube video using its ID.

    Args:
        video_id: The ID of the YouTube video.

    Returns:
        The language code (e.g., "en", "es", "fr") or None if an error occurs or the language is not found.
    """
    try:
        youtube = build("youtube", "v3", developerKey=settings.YOUTUBE_API_KEY)

        request = youtube.videos().list(
            part="snippet",  # We need the snippet part for language info
            id=video_id
        )
        response = request.execute()

        if response["items"]:
            snippet = response["items"][0]["snippet"]
            # Check for the 'defaultAudioLanguage' field first (more reliable)
            if "defaultAudioLanguage" in snippet:
                return snippet["defaultAudioLanguage"]
            else:
                return snippet.get("defaultLanguage", "en")  # Fallback to defaultLanguage or set a default

        else:
            return None  # Video not found

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_transcript(video_url: str) -> tuple:
    """
    Retrieves the transcript for a given YouTube video URL.

    Args:
        video_url (str): The URL of the YouTube video.

    Returns:
        tuple: A tuple containing a boolean indicating transcript availability, the transcript text, and the language code.
    """
    video_id = extract_video_id(video_url)
    if not video_id:
        log_exception(Exception("Invalid YouTube URL provided."), "get_transcript")
        return False, None, None
    
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    for transcript in transcript_list:
        language = transcript.language_code
        break

    try:
        log_exception(Exception(f"Trying to get transcript with language: {language}"), "get_transcript")
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        transcript = TextFormatter().format_transcript(transcript)
        with_transcript = True
    except Exception as e:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = TextFormatter().format_transcript(transcript)
            with_transcript = True
            return with_transcript, transcript, language
        except Exception as fallback_e:
            with_transcript = False
            transcript = None
            log_exception(fallback_e, f"Fallback attempt failed - Video ID: {video_id}")
            raise ValueError(f"Transcript is unavailable for video ID: {video_id}")
        

    return with_transcript, transcript, language