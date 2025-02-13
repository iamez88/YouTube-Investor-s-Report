import pytest
from unittest.mock import patch
from httpx import AsyncClient, ASGITransport
from app.main import app

@patch('app.api.endpoints.summarize_youtube_video')
@pytest.mark.asyncio
async def test_summarize_success(mock_summarize):
    # Arrange
    mock_summarize.return_value = ("This is a mock summary.", "en")
    request_data = {"youtube_url": "https://www.youtube.com/watch?v=YpEH8KPmi8I"}

    # Act
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/summarize", json=request_data)

    # Assert
    assert response.status_code == 200
    response_json = response.json()
    assert "summary" in response_json
    assert "language" in response_json
    assert response_json["summary"] == "This is a mock summary."
    assert response_json["language"] == "en"

# @patch('app.api.endpoints.summarize_youtube_video')
# @pytest.mark.asyncio
# async def test_summarize_invalid_url(mock_summarize):
#     # Arrange
#     mock_summarize.side_effect = ValueError("Transcript is unavailable for the provided YouTube URL.")
#     request_data = {"youtube_url": "invalid_url"}

#     # Act
#     async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
#         response = await ac.post("/api/summarize", json=request_data)

#     # Assert
#     assert response.status_code == 400
#     assert response.json()["detail"] == "Transcript is unavailable for the provided YouTube URL."
