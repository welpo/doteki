import logging
import os
import re
from typing import Any

import requests

DEFAULT_DATA_TYPE = "artists"
DEFAULT_INCLUDE_LINKS = True
DEFAULT_N = 1
DEFAULT_PERIOD = "7day"
VALID_PERIODS = ["overall", "7day", "1month", "3month", "6month", "12month"]
VALID_TYPES = ["artists", "tracks", "tags", "albums"]


def run(settings: dict[str, Any]) -> str | list[str] | None:
    if not validate_settings(settings):
        return None

    username = settings.get("username")
    data_type = settings.get("type", DEFAULT_DATA_TYPE)
    include_links = settings.get("include_links", DEFAULT_INCLUDE_LINKS)
    n = settings.get("n", DEFAULT_N)
    period = settings.get("period", DEFAULT_PERIOD)
    api_key = os.getenv("DOTEKI_LASTFM_API_KEY")
    if not api_key:
        logging.error("No DOTEKI_LASTFM_API_KEY environment variable found")
        return None
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettop{data_type}&user={username}&period={period}&api_key={api_key}&format=json"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        safe_error_message = str(e).replace(api_key, "HIDDEN_API_KEY")
        logging.error(f"Error fetching data from Last.fm: {safe_error_message}")
        return None

    data = response.json()
    top_items_key = f"top{data_type}"
    items_key = data_type[:-1]
    if top_items_key not in data or not data[top_items_key].get(items_key, []):
        logging.warning(f"No items found for user '{username}' in Last.fm data")
        return None
    top_items = data[top_items_key][items_key]
    top_items_formatted = [
        format_item(item, data_type, include_links) for item in top_items[:n]
    ]
    return top_items_formatted if n != 1 else top_items_formatted[0]


def validate_settings(settings: dict[str, Any]) -> bool:
    validation_results = []  # Ensures all errors are logged.
    validation_results.append(validate_period(settings.get("period")))
    validation_results.append(validate_type(settings.get("type")))
    validation_results.append(validate_n(settings.get("n")))
    validation_results.append(validate_username(settings.get("username")))
    return all(validation_results)


def validate_period(period: Any) -> bool:
    if period is None:
        return True
    if period not in VALID_PERIODS:
        logging.error(
            f"Invalid value for period: '{period}'. Valid options are: {', '.join(VALID_PERIODS)}"
        )
        return False
    return True


def validate_type(data_type: Any) -> bool:
    if data_type is None:
        return True
    if data_type not in VALID_TYPES:
        logging.error(
            f"Invalid value for data_type: '{data_type}'. Valid options are: {', '.join(VALID_TYPES)}"
        )
        return False
    return True


def validate_n(n: Any) -> bool:
    if n is None:
        return True
    if not isinstance(n, int) or n < 1:
        logging.error(f"Invalid value for n: '{n}'. n must be a positive integer")
        return False
    return True


def validate_include_links(include_links: Any) -> bool:
    if include_links is None:
        return True
    if not isinstance(include_links, bool):
        logging.error("Invalid value for 'include_links'. Expected boolean")
        return False
    return True


def validate_username(username: Any) -> bool:
    username_regex = r"^[a-zA-Z][a-zA-Z0-9_-]{1,14}$"
    if username is None:
        logging.error("No 'username' provided for lastfm plugin")
        return False
    elif not isinstance(username, str):
        logging.error("Invalid type for 'username'. Expected str")
        return False
    elif not re.match(username_regex, username):
        logging.error(
            "Invalid lastfm 'username'. It must be 2-15 characters long, begin with a letter, and contain only letters, numbers, '_' or '-'"
        )
        return False

    return True


def format_item(item: dict[str, Any], data_type: str, include_links: bool) -> str:
    name = item["name"]
    if data_type in ["albums", "tracks"]:
        artist_name = item["artist"]["name"]
        if include_links:
            artist_url = item["artist"]["url"]
            url = item["url"]
            return f"[{artist_name}]({artist_url}) - [{name}]({url})"
        else:
            return f"{artist_name} - {name}"
    else:
        return f"[{name}]({item['url']})" if include_links else str(name)
