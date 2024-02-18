import logging
import pyfiglet  # type: ignore
from typing import Any


def run(settings: dict[str, Any]) -> str | None:

    if not validate_settings(settings):
        return None
    text = settings.get("ascii_text")
    text = str(text)  ## In case is int number
    font = settings.get("font", "standard")
    result = pyfiglet.figlet_format(text, font)
    pre_text = "```text\n"
    post_text = "\n```"
    result = pre_text + result.rstrip() + post_text
    return str(result)


def validate_settings(settings: dict[str, Any]) -> bool:

    text = settings.get("ascii_text")
    font = settings.get("font", "standard")

    errors = []

    # Check required setting.
    if "ascii_text" not in settings:
        errors.append("No text provided for the FIGlet plugin")

    try:
        pyfiglet.figlet_format("test", font)

    except pyfiglet.FontNotFound:
        errors.append("Invalid font for the FIGlet plugin")

    if errors:
        for error in errors:
            logging.error(error)
        return False

    return True
