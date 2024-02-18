import logging
import pyfiglet  # type: ignore
from typing import Any


def run(settings: dict[str, Any]) -> str | None:
    if not validate_settings(settings):
        return None

    text = str(settings.get("ascii_text"))
    font = settings.get("font", "standard")

    try:
        result = pyfiglet.figlet_format(text, font)
    except pyfiglet.FontNotFound:
        logging.error("Invalid font for the FIGlet plugin")
        return None

    result_lines = result.splitlines()
    trimmed_result_lines = trim_leading_and_trailing_empty_lines(result_lines)
    result = "\n".join(trimmed_result_lines)

    pre_text = "```text\n"
    post_text = "\n```"
    result = pre_text + result.rstrip() + post_text
    return str(result)


def validate_settings(settings: dict[str, Any]) -> bool:
    # Check required setting.
    if "ascii_text" not in settings:
        logging.error("No text provided for the FIGlet plugin")
        return False

    return True


def trim_leading_and_trailing_empty_lines(lines: list[str]) -> list[str]:
    # Leading lines.
    while lines and lines[0].strip() == "":
        lines.pop(0)

    # Trailing lines.
    while lines and lines[-1].strip() == "":
        lines.pop()

    return lines
