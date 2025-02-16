import logging
from datetime import datetime
from typing import Any, Optional

import feedparser
import requests

DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_N = 5
DEFAULT_SEPARATOR = "·"
DEFAULT_SORT_FIELD = "published"
DEFAULT_SORT_ORDER = "descending"  # Only used if sort_field is set.


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
    sort_field = settings.get("sort_field", DEFAULT_SORT_FIELD)

    entries = feed.entries
    if sort_field := settings.get("sort_field"):
        sort_order = settings.get("sort_order", DEFAULT_SORT_ORDER)
        entries = sort_entries(entries, sort_field, sort_order)

    entries = entries[:n]
    formatted_entries = [
        format_entry(entry, separator, date_format, show_date, sort_field)
        for entry in entries
    ]
    return formatted_entries if n != 1 else formatted_entries[0]


def validate_settings(settings: dict[str, Any]) -> bool:
    expected_types = {
        "url": str,  # Required
        "n": int,  # Optional
        "show_date": bool,  # Optional
        "separator": str,  # Optional
        "date_format": str,  # Optional
        "sort_order": str,  # Optional
        "sort_field": str,  # Optional
    }
    valid_sort_orders = {"ascending", "descending"}
    valid_sort_fields = {"published", "updated"}
    errors = []
    if "url" not in settings:
        errors.append("No url provided for the Feed plugin")
    for setting, value in settings.items():
        expected_type = expected_types.get(setting)
        if expected_type and not isinstance(value, expected_type):
            errors.append(
                f"Invalid type for {setting}: '{type(value).__name__}'. Expected {expected_type.__name__}"
            )

        if setting == "sort_order" and value not in valid_sort_orders:
            errors.append(
                f"Invalid sort_order: '{value}'. Must be one of {valid_sort_orders}"
            )

        if setting == "sort_field" and value not in valid_sort_fields:
            errors.append(
                f"Invalid sort_field: '{value}'. Must be one of {valid_sort_fields}"
            )

    if errors:
        for error in errors:
            logging.error(error)
        return False

    return True


def sort_entries(entries: list, sort_field: str, sort_order: str) -> list:
    def get_sort_key(entry):
        date_tuple = get_entry_date(entry, sort_field)
        if date_tuple:
            return datetime(*date_tuple[:6])
        # Entries without dates at the end.
        return datetime.min if sort_order == "descending" else datetime.max

    reverse = sort_order == "descending"
    return sorted(entries, key=get_sort_key, reverse=reverse)


def get_entry_date(entry: dict[str, Any], field: str) -> Optional[tuple]:
    primary_field = f"{field}_parsed"
    fallback_field = "published_parsed" if field == "updated" else "updated_parsed"
    date_tuple = entry.get(primary_field)
    if date_tuple is None:
        date_tuple = entry.get(fallback_field)
    return date_tuple


def format_entry(
    entry: dict[str, Any],
    separator: str,
    date_format: str,
    show_date: bool,
    sort_field: str = "published",
) -> str:
    title = get_entry_data(entry, "title", "No Title")
    link = get_entry_data(entry, "link", "")
    date_str = get_formatted_date(entry, date_format, show_date, sort_field)

    separator_str = f" {separator} " if date_str else ""
    return f"[{title}]({link}){separator_str}{date_str}"


def get_entry_data(entry: dict[str, Any], key: str, default: str) -> str:
    if key in entry:
        return str(entry[key])
    else:
        logging.warning(f"Entry missing {key}")
        return default


def get_formatted_date(
    entry: dict[str, Any],
    date_format: str,
    show_date: bool,
    sort_field: str = "published",
) -> str:
    if not show_date:
        return ""
    date_tuple = get_entry_date(entry, sort_field)
    if date_tuple:
        return datetime(*date_tuple[:6]).strftime(date_format)
    logging.warning("Entry missing date")
    return ""
