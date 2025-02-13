import pytest
from unittest.mock import patch
from app.services.summarization_service import summarize_youtube_video

@patch('app.services.summarization_service.get_transcript')
def test_summarize_youtube_video_valid(mock_get_transcript):
    # Arrange
    mock_get_transcript.return_value = (True, "This is a mock transcript.", "en")
    
    # Act
    summary, language = summarize_youtube_video("https://www.youtube.com/watch?v=YpEH8KPmi8I")
    
    # Assert
    assert isinstance(summary, str)
    assert isinstance(language, str)
    assert summary == "This is a summary of the video transcript."
    assert language == "en"

@patch('app.services.summarization_service.get_transcript')
def test_summarize_youtube_video_invalid(mock_get_transcript):
    # Arrange
    mock_get_transcript.return_value = (False, None, None)
    
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        summarize_youtube_video("invalid_url")
    assert str(exc_info.value) == "Transcript is unavailable for the provided YouTube URL."
