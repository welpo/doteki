import logging
import sys
from unittest.mock import Mock, mock_open, patch

import pytest

from doteki.cli import (
    DEFAULT_CREDITS,
    SectionContext,
    find_section_indices,
    format_bullet_list,
    format_comma_and,
    format_glue,
    format_numbered_list,
    format_space,
    get_plugin_output,
    load_config,
    main,
    read_file_content,
    replace_section_content,
    update_readme_content,
    write_file_content,
)


def test_load_config_with_missing_file(caplog):
    missing_file_path = "nonexistent_config.toml"
    with patch("os.path.exists", return_value=False):
        with caplog.at_level(logging.ERROR):
            with pytest.raises(SystemExit):
                load_config(missing_file_path)

    assert "File not found" in caplog.text
    assert missing_file_path in caplog.text


def test_load_config_with_invalid_toml(caplog):
    invalid_toml_content = "<<invalid TOML content>>".encode()
    config_path = "invalid_config.toml"

    with patch("builtins.open", mock_open(read_data=invalid_toml_content)):
        with patch("os.path.exists", return_value=True):
            with caplog.at_level(logging.ERROR):
                with pytest.raises(SystemExit):
                    load_config(config_path)

    assert "Error parsing TOML file" in caplog.text


def test_load_valid_config_adds_credits():
    valid_toml_content = """
    [sections.favourite_quote]
    plugin = "random_choice"
    prepend_text = "> "
    options = [
        "Quote 1",
        "Quote 2",
        "Quote 3"
    ]

    [sections.blog]
    plugin = "feed"
    url = "https://example.com/feed.xml"
    n = 8
    """.encode()  # Encode the valid TOML content as bytes.

    expected_config = {
        "sections": {
            "favourite_quote": {
                "plugin": "random_choice",
                "prepend_text": "> ",
                "options": ["Quote 1", "Quote 2", "Quote 3"],
            },
            "blog": {"plugin": "feed", "url": "https://example.com/feed.xml", "n": 8},
        }
    }

    with patch("builtins.open", mock_open(read_data=valid_toml_content)):
        with patch("os.path.exists", return_value=True):
            config = load_config("dummy_config.toml")

    assert config == expected_config


def test_update_readme_no_plugin_specified(caplog):
    section_context = SectionContext("test_section", {}, "README.md")
    global_config = {}
    with caplog.at_level(logging.ERROR):
        update_readme_content(section_context, global_config)
    assert "No plugin specified for section 'test_section'" in caplog.text


@pytest.fixture
def readme_file(tmp_path):
    readme_path = tmp_path / "README.md"
    readme_path.write_text("Sample README content", encoding="utf-8")
    return readme_path


def test_update_readme_content_no_plugin_specified(caplog):
    section_context = SectionContext(
        name="test_section", settings={}, readme_path="README.md"
    )
    global_config = {}
    with caplog.at_level(logging.ERROR):
        update_readme_content(section_context, global_config)
    assert "No plugin specified for section 'test_section'" in caplog.text


@patch("doteki.cli.read_file_content")
def test_readme_content_read(mock_read_file_content, readme_file):
    mock_read_file_content.return_value = readme_file.read_text(encoding="utf-8")
    section_context = SectionContext(
        "test_section", {"plugin": "test_plugin"}, str(readme_file)
    )
    global_config = {}
    update_readme_content(section_context, global_config)
    mock_read_file_content.assert_called_once_with(str(readme_file))


def test_read_file_content_io_error(caplog):
    test_filepath = "nonexistent_file.txt"
    error_message = "mocked error"

    with patch("builtins.open", side_effect=IOError(error_message)):
        with caplog.at_level(logging.ERROR):
            content = read_file_content(test_filepath)

    assert content == ""
    assert (
        f"An error occurred while reading {test_filepath}: {error_message}"
        in caplog.text
    )


def test_find_section_indices_mismatched_markers(caplog):
    test_content = (
        "Start <!-- blog start --> Middle <!-- blog start --> End <!-- blog end -->"
    )
    section = "blog"
    marker_format = "<!-- {name} {position} -->"

    with caplog.at_level(logging.ERROR):
        indices = find_section_indices(test_content, section, marker_format)

    assert indices == []
    assert "Mismatched markers for section 'blog'" in caplog.text


@patch("doteki.cli.get_plugin_output", return_value=None)
@patch("doteki.cli.find_section_indices", return_value=[(0, 10)])
@patch("doteki.cli.read_file_content")
def test_handle_none_plugin_output(
    mock_read_file_content,
    mock_find_section_indices,
    mock_get_plugin_output,
    caplog,
    readme_file,
):
    mock_read_file_content.return_value = readme_file.read_text(encoding="utf-8")
    section_context = SectionContext(
        "test_section", {"plugin": "test_plugin"}, str(readme_file)
    )
    global_config = {}
    with caplog.at_level(logging.ERROR):
        update_readme_content(section_context, global_config)
    assert (
        "No content returned by plugin 'test_plugin' for section 'test_section'"
        in caplog.text
    )


def test_get_plugin_output_import_error(caplog):
    plugin_name = "nonexistent_plugin"
    with patch("importlib.import_module", side_effect=ImportError("mocked error")):
        assert get_plugin_output(plugin_name, {}) is None
        assert f"Missing dependency for plugin '{plugin_name}'" in caplog.text


def test_get_plugin_output_attribute_error(caplog):
    plugin_name = "incomplete_plugin"
    with patch("importlib.import_module", return_value=Mock(spec=[])):
        assert get_plugin_output(plugin_name, {}) is None
        assert f"Plugin '{plugin_name}' does not have a 'run' function" in caplog.text


def test_get_plugin_output_general_exception(caplog):
    plugin_name = "faulty_plugin"
    with patch(
        "importlib.import_module",
        return_value=Mock(run=Mock(side_effect=Exception("mocked error"))),
    ):
        assert get_plugin_output(plugin_name, {}) is None
        assert f"An error occurred in plugin '{plugin_name}'" in caplog.text


def test_format_comma_and_single_item():
    test_list = ["Oblómov"]
    expected_output = "Oblómov"
    assert format_comma_and(test_list) == expected_output


def test_format_comma_and_multiple_items():
    test_list = ["Oblómov", "Mírgorod", "Dead Souls"]
    expected_output = "Oblómov, Mírgorod, and Dead Souls"
    assert format_comma_and(test_list) == expected_output


def test_format_comma_and_empty_list():
    test_list = []
    expected_output = ""
    assert format_comma_and(test_list) == expected_output


def test_format_comma_and_empty():
    assert format_comma_and([]) == ""


def test_format_bullet_list_multiple_items():
    test_list = ["item1", "item2", "item3"]
    expected_output = "- item1\n- item2\n- item3"
    assert format_bullet_list(test_list) == expected_output


def test_format_bullet_list_single_item():
    test_list = ["single_item"]
    expected_output = "- single_item"
    assert format_bullet_list(test_list) == expected_output


def test_format_bullet_list_empty():
    test_list = []
    expected_output = ""
    assert format_bullet_list(test_list) == expected_output


def test_format_numbered_list_multiple_items():
    test_list = ["apple", "banana", "cherry"]
    expected_output = "1. apple\n2. banana\n3. cherry"
    assert format_numbered_list(test_list) == expected_output


def test_format_numbered_list_single_item():
    test_list = ["only_item"]
    expected_output = "1. only_item"
    assert format_numbered_list(test_list) == expected_output


def test_format_numbered_list_empty():
    test_list = []
    expected_output = ""
    assert format_numbered_list(test_list) == expected_output


def test_format_space_multiple_items():
    test_list = ["alpha", "beta", "gamma"]
    expected_output = "alpha beta gamma"
    assert format_space(test_list) == expected_output


def test_format_space_single_item():
    test_list = ["singleton"]
    expected_output = "singleton"
    assert format_space(test_list) == expected_output


def test_format_space_empty():
    test_list = []
    expected_output = ""
    assert format_space(test_list) == expected_output


def test_format_glue_multiple_items():
    test_list = ["part1", "part2", "part3"]
    expected_output = "part1part2part3"
    assert format_glue(test_list) == expected_output


def test_format_glue_single_item():
    test_list = ["singlepart"]
    expected_output = "singlepart"
    assert format_glue(test_list) == expected_output


def test_format_glue_empty():
    test_list = []
    expected_output = ""
    assert format_glue(test_list) == expected_output


def test_replace_section_content():
    original_content = "<!-- section start -->Hello<!-- section end -->, world"
    start_index = original_content.find("Hello")
    end_index = start_index + len("Hello")
    new_content = "Goodbye"

    updated_content = replace_section_content(
        original_content, new_content, start_index, end_index, inline=True
    )

    expected_content = "<!-- section start -->Goodbye<!-- section end -->, world"
    assert updated_content == expected_content


def test_write_file_content_ioerror(caplog):
    filepath = "test_file.txt"
    content = "Test content"
    with patch("builtins.open", mock_open()) as mock_file:
        mock_file.side_effect = IOError("Mocked IOError")
        write_file_content(filepath, content)
        assert f"An error occurred while writing to {filepath}" in caplog.text


def test_main_functionality_inline(tmp_path):
    readme_file = tmp_path / "README.md"
    config_file = tmp_path / "config.toml"
    readme_file.write_text(
        "<!-- mock start -->Old Content<!-- mock end -->", encoding="utf-8"
    )
    config_file.write_text(
        """
    [sections]
    [sections.mock]
    plugin = "current_date"
    inline = true
    """,
        encoding="utf-8",
    )

    test_args = ["doteki", "-c", str(config_file), "-i", str(readme_file)]
    with patch.object(sys, "argv", test_args):
        # Mock plugin output.
        with patch("doteki.plugins.current_date.run", return_value="2053-12-31"):
            main()

            updated_readme = readme_file.read_text(encoding="utf-8")
            assert "Old Content" not in updated_readme
            assert "<!-- mock start -->2053-12-31<!-- mock end -->" in updated_readme


def test_main_functionality_custom_marker_format(tmp_path):
    readme_file = tmp_path / "README.md"
    config_file = tmp_path / "config.toml"
    readme_file.write_text(
        "<!-- [mock:start] -->Old Content<!-- [mock:end] -->", encoding="utf-8"
    )
    config_file.write_text(
        """
    marker_format = "<!-- [{name}:{position}] -->"
    [sections]
    [sections.mock]
    plugin = "current_date"
    """,
        encoding="utf-8",
    )

    test_args = ["doteki", "-c", str(config_file), "-i", str(readme_file)]
    with patch.object(sys, "argv", test_args):
        with patch("doteki.plugins.current_date.run", return_value="2053-12-31"):
            main()
            updated_readme = readme_file.read_text(encoding="utf-8")
            assert "Old Content" not in updated_readme
            assert (
                "<!-- [mock:start] -->\n2053-12-31\n<!-- [mock:end] -->"
                in updated_readme
            )


def test_main_functionality_list(tmp_path):
    readme_file = tmp_path / "README.md"
    config_file = tmp_path / "config.toml"
    readme_file.write_text("<!-- lastfm start --><!-- lastfm end -->", encoding="utf-8")
    config_file.write_text(
        """
    [sections]
    [sections.lastfm]
    plugin = "lastfm"
    inline = false
    n = 3
    """,
        encoding="utf-8",
    )

    test_args = ["doteki", "-c", str(config_file), "-i", str(readme_file)]
    with patch.object(sys, "argv", test_args):
        with patch(
            "doteki.plugins.lastfm.run",
            return_value=[
                "[Yeat](https://www.last.fm/music/Yeat)",
                "[Caroline Polachek](https://www.last.fm/music/Caroline+Polachek)",
                "[Arthur Rubinstein](https://www.last.fm/music/Arthur+Rubinstein)",
            ],
        ):
            main()

            updated_readme = readme_file.read_text(encoding="utf-8")
            assert "Old Content" not in updated_readme
            assert (
                "<!-- lastfm start -->\n- [Yeat](https://www.last.fm/music/Yeat)\n- [Caroline Polachek](https://www.last.fm/music/Caroline+Polachek)\n- [Arthur Rubinstein](https://www.last.fm/music/Arthur+Rubinstein)\n<!-- lastfm end -->"
                in updated_readme
            )


def test_main_add_credits(tmp_path):
    readme_file = tmp_path / "README.md"
    config_file = tmp_path / "config.toml"
    readme_file.write_text(
        "<!-- mock start -->Old Content<!-- mock end -->", encoding="utf-8"
    )
    config_file.write_text(
        """
    [sections]
    [sections.mock]
    plugin = "current_date"
    inline = true
    """,
        encoding="utf-8",
    )

    test_args = ["doteki", "-c", str(config_file), "-i", str(readme_file)]
    with patch.object(sys, "argv", test_args):
        with patch("doteki.plugins.current_date.run", return_value="2053-12-31"):
            main()
            updated_readme = readme_file.read_text(encoding="utf-8")
            assert "Old Content" not in updated_readme
            assert "<!-- mock start -->2053-12-31<!-- mock end -->" in updated_readme
            assert DEFAULT_CREDITS in updated_readme


def test_main_dont_add_existing_credits(tmp_path):
    readme_file = tmp_path / "README.md"
    config_file = tmp_path / "config.toml"
    original_readme = "<!-- mock start -->2053-12-31<!-- mock end -->\nPowered by [doteki](https://doteki.org)"
    readme_file.write_text(original_readme, encoding="utf-8")
    config_file.write_text(
        """
    credits = "Powered by [doteki](https://doteki.org)"
    [sections]
    [sections.mock]
    plugin = "current_date"
    inline = true
    """,
        encoding="utf-8",
    )

    test_args = ["doteki", "-c", str(config_file), "-i", str(readme_file)]
    with patch.object(sys, "argv", test_args):
        with patch("doteki.plugins.current_date.run", return_value="2053-12-31"):
            main()
            updated_readme = readme_file.read_text(encoding="utf-8")
            assert updated_readme == original_readme


def test_main_disabled_credits(tmp_path):
    readme_file = tmp_path / "README.md"
    config_file = tmp_path / "config.toml"
    original_readme = "<!-- mock start -->2053-12-31<!-- mock end -->"
    readme_file.write_text(original_readme, encoding="utf-8")
    config_file.write_text(
        """
    credits = ""
    [sections]
    [sections.mock]
    plugin = "current_date"
    inline = true
    """,
        encoding="utf-8",
    )

    test_args = ["doteki", "-c", str(config_file), "-i", str(readme_file)]
    with patch.object(sys, "argv", test_args):
        with patch("doteki.plugins.current_date.run", return_value="2053-12-31"):
            main()
            updated_readme = readme_file.read_text(encoding="utf-8")
            assert updated_readme == original_readme


def test_replace_default_credits_with_custom_credits(tmp_path):
    # Initial setup with default credits
    readme_file = tmp_path / "README.md"
    config_file = tmp_path / "config.toml"
    custom_credits = "dōteki is the best"
    original_readme = f"<!-- mock start --><!-- mock end -->\n{DEFAULT_CREDITS}"
    readme_file.write_text(original_readme, encoding="utf-8")

    # Custom credits configuration
    config_file.write_text(
        f"""
    credits = "a{custom_credits}"
    [sections]
    [sections.mock]
    plugin = "current_date"
    inline = true
    """,
        encoding="utf-8",
    )

    test_args = ["doteki", "-c", str(config_file), "-i", str(readme_file)]
    with patch.object(sys, "argv", test_args):
        with patch("doteki.plugins.current_date.run", return_value="2053-12-31"):
            main()
            updated_readme = readme_file.read_text(encoding="utf-8")
            # Default credits should be gone.
            print(updated_readme)
            assert custom_credits in updated_readme
            assert DEFAULT_CREDITS not in updated_readme
