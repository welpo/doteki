import logging
from datetime import datetime
from unittest.mock import patch

from doteki.plugins.current_date import run


def test_logging_invalid_date_format(caplog):
    settings = {"format": 123}
    with caplog.at_level(logging.ERROR):
        result = run(settings)
    assert "Invalid type for date format" in caplog.text
    assert result is None


def test_default_date_format():
    settings = {}
    with patch("doteki.plugins.current_date.datetime") as mock_date:
        mock_date.now.return_value = datetime(2015, 10, 21)
        result = run(settings)
    assert result == "2015-10-21"


def test_custom_american_date_format():
    settings = {"format": "%m/%d/%Y"}
    with patch("doteki.plugins.current_date.datetime") as mock_date:
        mock_date.now.return_value = datetime(2015, 10, 21)
        result = run(settings)
    assert result == "10/21/2015"


def test_full_date_with_day():
    settings = {"format": "%A, %B %d, %Y"}
    with patch("doteki.plugins.current_date.datetime") as mock_date:
        mock_date.now.return_value = datetime(2015, 10, 21)
        result = run(settings)
    assert result == "Wednesday, October 21, 2015"


def test_date_sans_percent_warn(caplog):
    settings = {"format": "year-month-day"}
    result = run(settings)
    assert result is not None
    assert result == "year-month-day"
    assert (
        "The date format 'year-month-day' does not contain a '%' character"
        in caplog.text
    )
