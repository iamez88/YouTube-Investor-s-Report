from fastapi import APIRouter, HTTPException
from app.services.summarization_service import summarize_youtube_video
from pydantic import BaseModel, field_validator
import re

router = APIRouter()

class SummarizeRequest(BaseModel):
    youtube_url: str

    @field_validator('youtube_url')
    def validate_youtube_url(cls, v):
        youtube_regex = (
            r'(https?://)?(www\.)?'
            r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        if not re.match(youtube_regex, v):
            raise ValueError('Invalid YouTube URL')
        return v

class SummarizeResponse(BaseModel):
    summary: str
    language: str

@router.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):
    try:
        summary, language = summarize_youtube_video(request.youtube_url)
        return SummarizeResponse(summary=summary, language=language)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
