from google import genai
import logging
from app.utils.helpers import log_exception
from app.data_ingestion.transcript import get_transcript
from app.core.config import settings


def summarize_youtube_video(youtube_url: str) -> tuple:
    try:
        with_transcript, transcript, language = get_transcript(youtube_url)
        if not with_transcript:
            raise ValueError("Transcript is unavailable for the provided YouTube URL.")
        summary, language = report_youtube_stocks_markets(youtube_url, transcript, language)
        return summary, language
    except Exception as e:
        log_exception(e, "summarize_youtube_video")
        raise e

def report_youtube_stocks_markets(video_url: str, transcript: str, language: str) -> tuple:
    """
    Summarizes the YouTube video based on its transcript.

    Args:
        video_url (str): The URL of the YouTube video.
        transcript (str, optional): Pre-provided transcript. Defaults to None.

    Returns:
        tuple: The prompt used and the generated response.
    """
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    if language and language.lower().startswith("en"):
        prompt = f"""
Task:
You will be provided with a transcript of a YouTube video discussing stocks and the market. Your task is to analyze the transcript carefully and generate a structured, detailed report summarizing the key insights. Ensure that your analysis remains factual and is strictly based on the transcript provided.

Instructions:
- Summarize the main points covered in the video. Extract key insights related to market trends, investment strategies, risks, or recommendations.
- Identify and list all specific stocks, companies, and ETFs discussed in the video. Provide relevant supporting context, such as reasons for their mention, predictions, actions taken and opinions. If any recommendations are provided, summarize them clearly.
- Report any technical analysis that mentions the support, resistance level, as well as buy or sell triggers. 
- Highlight any statistics, figures, or data points mentioned. 
- Please be concise with your reporting and ensure your response format is structured and consistent.

Note: Use proper markdown syntax:
- Use # for main heading
- Use ## for subheadings
- Use * or - for bullet points
- Use ** for bold text
- Use * for italic text
- Use ``` for code blocks
- Properly escape any special characters

Transcript: {transcript}

            """
    else:
        prompt = f"""
You will be provided with a transcript of a YouTube video, discussing stocks and the market. Your task is to analyze the transcript carefully and generate a structured, detailed report summarizing the key insights. Ensure that your analysis remains factual and is strictly based on the transcript provided.

Instructions:
- Summarize the main points covered in the video. Extract key insights related to market trends, investment strategies, risks, or recommendations.
- Identify and list all specific stocks, companies, and ETFs discussed in the video. Provide relevant supporting context, such as reasons for their mention, predictions, actions taken and opinions. If any recommendations are provided, summarize them clearly.
- Report any technical analysis that mentions the support, resistance level, as well as buy or sell triggers. 
- Highlight any statistics, figures, or data points mentioned.
- Provide your report in the language found within the transcript.   
- Please be concise with your reporting and ensure your response format is structured and consistent.

Note: Use proper markdown syntax:
- Use # for main heading
- Use ## for subheadings
- Use * or - for bullet points
- Use ** for bold text
- Use * for italic text
- Use ``` for code blocks
- Properly escape any special characters

Transcript: {transcript}
            """
    try:
        # Try generating content using Gemini 2.0 model
        response = client.models.generate_content(
            model="gemini-2.0-flash-thinking-exp-01-21",
            contents=prompt
        )
        logging.info("Generating response using Gemini 2.0...")
        print(response.text)
    except Exception as e:
        log_exception(e, "report_youtube_stocks_markets - Gemini 2.0")
        # Fallback to Gemini 1.5 model
        logging.info("Gemini 2.0 resource depleted, falling back to Gemini 1.5.")
        response = client.models.generate_content(
            model="gemini-1.5-pro",
            contents=prompt
        )
        print(response.text)

    return response.text, language
