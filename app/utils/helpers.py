from loguru import logger
import sys
from app.core.config import settings

def setup_logging():
    logger.remove()
    logger.add(sys.stdout, level=settings.LOG_LEVEL)
    logger.add("app.log", rotation="10 MB", level=settings.LOG_LEVEL)

def log_exception(e: Exception, context: str):
    logger.error(f"Exception in {context}: {e}")
