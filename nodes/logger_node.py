# Logger Node - Handles event logging
from logger import logger


def log_event(event_type: str, data: dict) -> None:

    try:
        logger.log(event_type, data)
    except Exception as e:
        print(f"Logging error: {str(e)}")


def save_logs() -> None:
    """Save all logs to file"""
    try:
        logger.save()
    except Exception as e:
        print(f"Failed to save logs: {str(e)}")
