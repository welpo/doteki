import logging
from datetime import datetime
from typing import Any

DEFAULT_FORMAT = "%Y-%m-%d"


def run(settings: dict[str, Any]) -> str | None:
    if not validate_settings(settings):
        return None
    date_format = settings.get("format", DEFAULT_FORMAT)
    current_date = datetime.now()
    return current_date.strftime(date_format)


def validate_settings(settings: dict[str, Any]) -> bool:
    date_format = settings.get("format")
    if date_format is None:
        return True  # We'll use the default.
    if not isinstance(date_format, str):
        logging.error(
            f"Invalid type for date format: '{date_format}'. Must be a string"
        )
        return False
    if "%" not in date_format:
        logging.warning(
            f"The date format '{date_format}' does not contain a '%' character. Double-check that you are using the correct format string"
        )
        # Since all strings evaluate to a valid date format, we proceed.
    return True
