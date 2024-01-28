import logging
from pyfiglet import figlet_format, FigletFont  # type: ignore
from html import escape
from typing import Any

DEFAULT_FONT = "standard"
DEFAULT_ASCII_TEXT = "<Your text here>"
PARAM_FONT = "font"
PARAM_ASCII_TEXT = "ascii_text"
PARAM_BOLD = "bold"


def run(settings: dict[str, Any]) -> str | None:
    if not validate_settings(settings):
        return None

    # Get parameters
    font = settings.get(PARAM_FONT)
    ascii_text = settings.get(PARAM_ASCII_TEXT)

    # Print help in README.md if no parameters found
    if font is None and ascii_text is None:
        return default_ascii_message()

    # Set default font if not exists
    if string_is_empty(font):
        font = DEFAULT_FONT

    # Store font names
    found_fonts = FigletFont.getFonts()

    # With font=list, show font names (and opt. with sample)
    if font == "list":
        if string_is_empty(ascii_text):
            return enumerate_fonts(found_fonts)
        else:
            return display_font_samples(found_fonts, ascii_text)

    # Other cases: set default string
    if string_is_empty(ascii_text):
        ascii_text = DEFAULT_ASCII_TEXT

    # Error if font not found
    if font not in found_fonts:
        logging.error(f"Font '{font}' not installed")
        return None

    # Go on!
    result = (
        "<pre style='background: none; border: none'>\n"
        + figlet_format(ascii_text, font)
        + "\n</pre>\n"
    )

    # Optional: bolder chars
    if settings.get(PARAM_BOLD, False) == True:
        result = "<b>\n" + result + "\n</b>\n"

    return result  # type: ignore


def validate_settings(settings: dict[str, Any]) -> bool:
    font = settings.get(PARAM_FONT)
    ascii_text = settings.get(PARAM_ASCII_TEXT)
    bold = settings.get(PARAM_BOLD, False)

    if not isinstance(bold, bool):
        logging.error(f"Invalid type for bold: '{bold}'. Must be a bool")
        return False

    if font is not None and not isinstance(font, str):
        logging.error(f"Invalid type for font: '{font}'. Must be a string")
        return False

    if ascii_text is not None and not isinstance(ascii_text, str):
        logging.error(f"Invalid type for ascii_text: '{ascii_text}'. Must be a string")
        return False
    return True


# None or empty string
def string_is_empty(text: str | None) -> bool:
    return text is None or text.strip() == ""


def default_ascii_message() -> str:
    return """

## Figlet plugin not configured    

### doteki.toml file example
<pre>
[sections.ascii_art]
plugin = "figlet"
font = "digital"
ascii_text = "&lt;Your text here&gt;"
bold = true
</pre>

### Optional fonts listing

You can list all the fonts with **font="list"** in **doteki.toml**

Adding an **ascii_text** you'll get also a sample for each.

Some fonts don't perform well in lowercase. You'll must experiment.

<pre>
font = "list"
ascii_text = "My sample"
</pre>
"""


def enumerate_fonts(fonts_list: list[str]) -> str:
    s = "## Figlet plugin fonts\n"
    s += ", ".join(fonts_list) + "\n"
    return s


def display_font_samples(found_fonts: list[str], ascii_text: str | None) -> str:
    ascii_text = str(ascii_text)  # mypy complain. Should not be None by previous logic
    ascii_text = (
        ascii_text.upper()
    )  # figlet fonts perform generally better in uppercase. Just for demonstration.
    result = ""
    for font in found_fonts:
        result += f"FONT: {font}\n"
        result += "\n<pre>"
        result += escape(
            figlet_format(ascii_text, font)
        )  # Must escape because of occasional rare characters
        result += "</pre>\n"
    return result
