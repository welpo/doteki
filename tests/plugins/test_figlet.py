import logging
#from datetime import datetime
#from unittest.mock import patch
from doteki.plugins.figlet import run

# Parameters
PARAM_FONT = "font"
PARAM_TEXT = "ascii_text"
PARAM_BOLD = "bold"

# Output with no parameters
DEFAULT_OUTPUT = "Figlet plugin not configured"

# This is "<Your text here>" in octal
DEFAULT_OCTAL_OUTPUT = "074 131 157 165 162  164 145 170 164  150 145 162 145 076 \n"

def test_figlet_no_parameters():
    settings = {}
    result = run(settings)
    assert DEFAULT_OUTPUT in result

def test_figlet_only_text():
    # IMPORTANT: r-string due to spurious escape sequences
    expected = r"""<pre style='background: none; border: none'>
                           _      
 ___  __ _ _ __ ___  _ __ | | ___ 
/ __|/ _` | '_ ` _ \| '_ \| |/ _ \
\__ \ (_| | | | | | | |_) | |  __/
|___/\__,_|_| |_| |_| .__/|_|\___|
                    |_|           

</pre>
"""
    settings = {PARAM_TEXT: 'sample'}
    result = run(settings)
    print(result)
    assert expected == result

# Only verifying it's a comma splitted list
def test_figlet_list_fonts():
    settings = {PARAM_FONT: 'list'}
    result = run(settings)
    counter = len(result.split(', '))
    assert counter > 0 

# Only verifying it's a collection of 'FONT:' headers
def test_figlet_list_fonts_with_text():
    settings = {PARAM_FONT: 'list', PARAM_TEXT: 'figlet'}
    result = run(settings)
    counter = len(result.split('FONT: '))
    assert counter > 0

# Verify simple fonts
def test_figlet_font_octal():
    settings = {PARAM_FONT: 'octal', PARAM_TEXT: ''}
    result = run(settings)
    assert DEFAULT_OCTAL_OUTPUT in result

# Verify simple fonts (with no ascii_text)
def test_figlet_font_octal_no_ascii_text():
    settings = {PARAM_FONT: 'octal'}
    result = run(settings)
    assert DEFAULT_OCTAL_OUTPUT in result

# Verify simple fonts: term
def test_figlet_font_term():
    settings = {PARAM_FONT: 'term', PARAM_TEXT: 'Just a test'}
    result = run(settings)
    assert 'Just a test\n' in result

# Settings with a list in font
def test_figlet_bad_parameter_font():
    settings = {PARAM_FONT: ['list']}
    result = run(settings)
    assert result is None

# Settings with a list in text
def test_figlet_bad_parameter_ascii_text():
    settings = {PARAM_TEXT: ['list']}
    result = run(settings)
    assert result is None

# Settings with bad font name
def test_figlet_bad_font():
    settings = {PARAM_FONT: 'not_a_valid_font'}
    result = run(settings)
    assert result is None

# Bold parameter
def test_figlet_bold():
    settings = {PARAM_BOLD: 'not boolean'}
    result = run(settings)
    assert result is None
