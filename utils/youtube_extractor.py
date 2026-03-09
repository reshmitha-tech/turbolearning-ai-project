import re
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url):
    """
    Extracts the video ID from a YouTube URL.
    """
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    if video_id_match:
        return video_id_match.group(1)
    return None

def extract_transcript_from_url(url):
    """
    Fetches and cleans the transcript from a YouTube video URL using an instance of YouTubeTranscriptApi.
    """
    video_id = extract_video_id(url)
    if not video_id:
        return None
    
    try:
        # Use instance-based logic as required by some versions of the library
        ytt_api = YouTubeTranscriptApi()
        
        # Fetch specifying English variants to be thorough
        transcript_data = ytt_api.fetch(video_id, languages=['en', 'en-GB', 'en-US'])
        
        # Access the 'text' attribute of each FetchedTranscriptSnippet object
        transcript_text = " ".join([item.text for item in transcript_data])
        
        return transcript_text.strip()
    except Exception as e:
        print(f"Error fetching YouTube transcript: {e}")
        return None
