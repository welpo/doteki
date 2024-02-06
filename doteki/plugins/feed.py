import logging
from datetime import datetime
from typing import Any

import feedparser
import requests

DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_N = 5
DEFAULT_SEPARATOR = "·"


def run(settings: dict[str, Any]) -> str | list[str] | None:
    if not validate_settings(settings):
        return None

    feed_url = settings["url"]

    try:
        response = requests.get(feed_url)
        response.raise_for_status()
        if not response.content:
            logging.error("The response from the URL is empty")
            return None
    except requests.exceptions.RequestException as e:
        logging.error("Error fetching the feed: {e}")
        return None

    try:
        feed = feedparser.parse(response.content)
        if not feed.entries:
            logging.error("Malformed feed: no entries found")
            return None
    except Exception as e:
        logging.error(f"Error processing the feed: {e}")
        return None

    date_format = settings.get("date_format", DEFAULT_DATE_FORMAT)
    show_date = settings.get("show_date", False)
    separator = settings.get("separator", DEFAULT_SEPARATOR)
    n = settings.get("n", DEFAULT_N)
    entries = feed.entries[:n]
    formatted_entries = [
        format_entry(entry, separator, date_format, show_date) for entry in entries
    ]
    return formatted_entries if n != 1 else formatted_entries[0]


def validate_settings(settings: dict[str, Any]) -> bool:
    expected_types = {
        "url": str,  # Required.
        "n": int,  # Optional.
        "show_date": bool,  # Optional.
        "separator": str,  # Optional.
        "date_format": str,  # Optional.
    }
    errors = []

    # Check required setting.
    if "url" not in settings:
        errors.append("No url provided for the Feed plugin")

    # Validate types of provided settings.
    for setting, value in settings.items():
        expected_type = expected_types.get(setting)
        if expected_type and not isinstance(value, expected_type):
            errors.append(
                f"Invalid type for {setting}: '{type(value).__name__}'. Expected {expected_type.__name__}"
            )

    if errors:
        for error in errors:
            logging.error(error)
        return False

    return True


def format_entry(
    entry: dict[str, Any], separator: str, date_format: str, show_date: bool
) -> str:
    title = get_entry_data(entry, "title", "No Title")
    link = get_entry_data(entry, "link", "")
    date_str = get_formatted_date(entry, date_format, show_date)

    separator_str = f" {separator} " if date_str else ""
    return f"[{title}]({link}){separator_str}{date_str}"


def get_entry_data(entry: dict[str, Any], key: str, default: str) -> str:
    if key in entry:
        return str(entry[key])
    else:
        logging.warning(f"Entry missing {key}")
        return default


def get_formatted_date(entry: dict[str, Any], date_format: str, show_date: bool) -> str:
    date_tuple = entry.get("published_parsed")
    if show_date and date_tuple:
        # Unpacks first six elements (year, month, day, hour, minute, second)
        # and formats them into a string.
        return datetime(*date_tuple[:6]).strftime(date_format)
    elif show_date:
        logging.warning("Entry missing date")
    return ""
