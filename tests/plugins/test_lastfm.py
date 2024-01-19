import json
import logging
import os
import pytest
import requests
from unittest.mock import Mock, MagicMock, patch
from doteki.plugins.lastfm import (
    format_item,
    run,
    validate_include_links,
    validate_n,
    validate_period,
    validate_settings,
    validate_type,
    validate_username,
)


def test_validate_settings_returns_none():
    settings = {
        "username": "invalid_username",
        "type": "invalid_type",
        "period": "invalid_period",
        "n": "invalid_n",
    }
    result = run(settings)
    assert result is None


@pytest.mark.parametrize(
    "input_value, expected",
    [
        (None, True),
        ("artists", True),
        ("albums", True),
        ("tracks", True),
        ("tags", True),
        ("songs", False),
    ],
)
def test_validate_type(input_value, expected):
    assert validate_type(input_value) == expected


def test_no_username(caplog):
    settings = {
        "type": "artists",
        "period": "7day",
        "n": 3,
    }
    with patch("requests.get") as mock_get:
        result = run(settings)
        assert result is None
        assert "No 'username' provided for lastfm plugin" in caplog.text


@pytest.mark.parametrize(
    "input_value, expected",
    [
        (None, True),
        ("7day", True),
        ("1month", True),
        ("3month", True),
        ("6month", True),
        ("12month", True),
        ("overall", True),
        ("forever", False),
    ],
)
def test_validate_period(input_value, expected):
    assert validate_period(input_value) == expected


@pytest.mark.parametrize(
    "input_value, expected",
    [(None, True), (True, True), (False, True), ("False", False)],
)
def test_validate_include_links(input_value, expected):
    assert validate_include_links(input_value) == expected


@pytest.mark.parametrize(
    "input_value, expected", [(None, True), (2, True), ("2", False)]
)
def test_validate_n(input_value, expected):
    assert validate_n(input_value) == expected


@pytest.mark.parametrize(
    "input_value, expected",
    [
        ("example", True),
        ("a", False),
        ("thisusernameiswaaaaaaytoolong", False),
        ("1example", False),
        ("example!", False),
    ],
)
def test_validate_username(input_value, expected):
    assert validate_username(input_value) == expected


@patch.dict(os.environ, {"DOTEKI_LASTFM_API_KEY": "mock_api_key"})
def test_default_period_used():
    settings = {
        "username": "example",
        "type": "artists",
        "n": 3,
    }
    with patch("requests.get") as mock_get:
        run(settings)
        assert f"&period={'7day'}" in mock_get.call_args[0][0]


def test_log_multiple_settings_errors(caplog):
    settings = {
        "username": 123,
        "type": "songs",
        "period": "forever",
        "n": "3",
    }

    with caplog.at_level(logging.ERROR):
        result = validate_settings(settings)

    assert not result
    assert "Invalid type for 'username'. Expected str" in caplog.text
    assert "Invalid value for data_type: 'songs'" in caplog.text
    assert "Invalid value for period: 'forever'" in caplog.text
    assert "Invalid value for n: '3'. n must be a positive integer" in caplog.text


@patch.dict(os.environ, {"DOTEKI_LASTFM_API_KEY": "mock_api_key"})
@pytest.mark.parametrize(
    "exception",
    [
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.HTTPError,
    ],
)
@patch("requests.get")
def test_lastfm_request_exceptions(mock_get, caplog, exception):
    mock_get.side_effect = exception
    settings = {
        "username": "example",
        "type": "artists",
        "period": "7day",
        "n": 3,
    }

    with caplog.at_level(logging.ERROR):
        result = run(settings)

    assert result is None
    assert "Error fetching data from Last.fm" in caplog.text


MOCK_ARTIST_JSON = """{"topartists":{"artist":[{"name":"Frankie Cosmos","playcount":102,"mbid":"28503ab7-8bf2-4666-a7bd-2644bfc7cb1d","url":"http://www.last.fm/music/Dream+Theater","streamable":1,"image":["...","...","..."]},{"name":"Patrice Rushen","playcount":66,"mbid":"unknown","url":"unknown","streamable":"unknown","image":["...","...","..."]},{"name":"Ana Frango Elétrico","playcount":52,"mbid":"unknown","url":"unknown","streamable":"unknown","image":["...","...","..."]}]}}"""


@patch.dict(os.environ, {"DOTEKI_LASTFM_API_KEY": "mock_api_key"})
@patch("requests.get")
def test_successful_lastfm_response(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = json.loads(MOCK_ARTIST_JSON)
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    settings = {
        "username": "example",
        "type": "artists",
        "period": "7day",
        "n": 3,
    }

    result = run(settings)

    assert result is not None
    assert len(result) == 3
    assert "[Frankie Cosmos](http://www.last.fm/music/Dream+Theater)" in result[0]
    assert "Patrice Rushen" in result[1]
    assert "Ana Frango Elétrico" in result[2]


@patch.dict(os.environ, {"DOTEKI_LASTFM_API_KEY": "mock_api_key"})
@patch("requests.get")
def test_lastfm_response_single_item_is_str(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = json.loads(MOCK_ARTIST_JSON)
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    settings = {
        "username": "example",
        "type": "artists",
        "period": "7day",
        "n": 1,
    }

    result = run(settings)

    assert isinstance(result, str)
    assert "[Frankie Cosmos](http://www.last.fm/music/Dream+Theater)" == result


def test_format_item_without_links():
    item = {"name": "Yeat", "url": "http://www.last.fm/music/Yeat"}
    result = format_item(item, "artists", include_links=False)
    assert result == "Yeat"
    assert "http://www.last.fm/music/Test+Artist" not in result


@patch.dict(os.environ, {}, clear=True)
@patch("requests.get")
def test_missing_api_key_warning(mock_get, caplog):
    mock_response = {
        "topartists": {
            "artist": [{"name": "Furyan", "url": "http://www.last.fm/music/Furyan"}]
        }
    }
    mock_get.return_value = Mock()
    mock_get.return_value.json.return_value = mock_response

    settings = {
        "username": "example",
        "type": "artists",
        "period": "7day",
        "n": 1,
    }

    with caplog.at_level(logging.ERROR):
        result = run(settings)
        assert result is None
        assert "No DOTEKI_LASTFM_API_KEY environment variable found" in caplog.text


@patch.dict(os.environ, {"DOTEKI_LASTFM_API_KEY": "SECRET_API_KEY"})
@patch("requests.get")
def test_api_key_hidden_in_error_message(mock_get, caplog):
    mock_get.side_effect = requests.exceptions.RequestException(
        "Error message containing SECRET_API_KEY"
    )

    settings = {
        "username": "example",
        "type": "artists",
        "period": "7day",
        "n": 1,
    }

    with caplog.at_level(logging.ERROR):
        result = run(settings)
        assert "HIDDEN_API_KEY" in caplog.text
        assert "SECRET_API_KEY" not in caplog.text


MOCK_ALBUM_JSON = """{"topalbums":{"album":[{"name":"Hexada","playcount":123,"mbid":"12345abcd-hexa-6789-ghij-klmnopqrst","url":"http://www.last.fm/music/Ghostemane/Hexada","artist":{"name":"Ghostemane","mbid":"54321dcba-hexa-9876-fehi-jklmnopqrst","url":"http://www.last.fm/music/Ghostemane"}},{"name":"Romantic Piano","playcount":98,"mbid":"abcde12345-roma-6789-pqrs-tuvwxyz","url":"http://www.last.fm/music/Gia+Margaret/Romantic+Piano","artist":{"name":"Gia Margaret","mbid":"edcba54321-roma-9876-srqp-zyxwvut","url":"http://www.last.fm/music/Gia+Margaret"}},{"name":"Giles Corey","playcount":150,"mbid":"123ab456cd-gile-7890-core-yz12345678","url":"http://www.last.fm/music/Giles+Corey/Giles+Corey","artist":{"name":"Giles Corey","mbid":"876zy54321-gile-0987-eryc-87654321012","url":"http://www.last.fm/music/Giles+Corey"}}]}}"""


@patch.dict(os.environ, {"DOTEKI_LASTFM_API_KEY": "mock_api_key"})
@patch("requests.get")
def test_successful_album_response(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = json.loads(MOCK_ALBUM_JSON)
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    settings = {
        "username": "example",
        "type": "albums",
        "period": "7day",
        "n": 2,
    }

    result = run(settings)

    assert result is not None
    assert len(result) == 2
    assert (
        "[Ghostemane](http://www.last.fm/music/Ghostemane) - [Hexada](http://www.last.fm/music/Ghostemane/Hexada)"
        in result[0]
    )
    assert (
        "[Gia Margaret](http://www.last.fm/music/Gia+Margaret) - [Romantic Piano](http://www.last.fm/music/Gia+Margaret/Romantic+Piano)"
        in result[1]
    )


def test_format_item_album_without_links():
    item = {
        "name": "Tungsten",
        "url": "https://www.last.fm/music/Healy/Tungsten",
        "artist": {
            "name": "Healy",
            "url": "https://www.last.fm/music/Healy",
        },
    }
    result = format_item(item, "albums", include_links=False)
    assert result == "Healy - Tungsten"
    assert "https://www.last.fm/music/Healy/Tungsten" not in result
    assert "https://www.last.fm/music/Healy" not in result


@patch.dict(os.environ, {"DOTEKI_LASTFM_API_KEY": "mock_api_key"})
def test_empty_artist_list_logs_warning(caplog):
    empty_artist_json = """{"topartists": {"artist": [], "@attr": {"user": "username", "totalPages": "0", "page": "1", "perPage": "50", "total": "0"}}}"""

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = json.loads(empty_artist_json)
        mock_get.return_value = mock_response

        settings = {
            "username": "username",
            "type": "artists",
            "period": "7day",
            "n": 3,
        }

        with caplog.at_level(logging.WARNING):
            result = run(settings)
            assert result is None
            assert "No items found for user 'username' in Last.fm data" in caplog.text


@patch.dict(os.environ, {"DOTEKI_LASTFM_API_KEY": "mock_api_key"})
def test_missing_top_artists_key(caplog):
    incomplete_json = """{"someOtherKey": {"data": []}}"""

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = json.loads(incomplete_json)
        mock_get.return_value = mock_response

        settings = {
            "username": "username",
            "type": "artists",
            "period": "7day",
            "n": 3,
        }

        with caplog.at_level(logging.WARNING):
            result = run(settings)
            assert result is None
            assert "No items found for user 'username' in Last.fm data" in caplog.text
