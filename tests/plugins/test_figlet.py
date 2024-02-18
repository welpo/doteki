import logging
from doteki.plugins.figlet import run, trim_leading_and_trailing_empty_lines


def test_default_font():
    settings = {"ascii_text": "hola"}
    expected = r""" _           _       
| |__   ___ | | __ _ 
| '_ \ / _ \| |/ _` |
| | | | (_) | | (_| |
|_| |_|\___/|_|\__,_|"""
    result = run(settings)
    assert expected in str(result)


def test_empty_text(caplog):
    settings = {"font": "standard"}
    with caplog.at_level(logging.ERROR):
        result = run(settings)
    assert result is None
    assert "No text provided for the FIGlet plugin" in caplog.text


# If invalid font, result is none
def test_invalid_font(caplog):
    settings = {"ascii_text": "hola", "font": "invalid_font"}
    with caplog.at_level(logging.ERROR):
        result = run(settings)
    assert result is None
    assert "Invalid font for the FIGlet plugin" in caplog.text


def test_int_text():
    settings = {"ascii_text": 42, "font": "standard"}
    expected = r""" _  _  ____  
| || ||___ \ 
| || |_ __) |
|__   _/ __/ 
   |_||_____|"""
    result = run(settings)
    assert expected in str(result)
