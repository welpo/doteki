import argparse
import contextlib
import importlib
import logging
import os
import re
import sys
from importlib.metadata import version
from typing import Any

import tomllib

DEFAULT_CREDITS = '<a href="https://doteki.org"><img src="https://img.shields.io/badge/powered_by-d%C5%8Dteki-0?style=flat-square&labelColor=202b2d&color=5E936C" align="right" alt="Powered by dōteki"></a>'
DEFAULT_MARKER_FORMAT = "<!-- {name} {position} -->"


def main() -> None:
    args = parse_arguments()
    logging.basicConfig(
        level=logging.INFO, format="[dōteki] %(levelname)s: %(message)s"
    )
    exit_if_file_missing(args.input)
    global_config = load_config(args.config)
    process_sections(global_config, args.input)
    insert_credits(global_config, args.input)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="dōteki: A tool to update README sections with plugins defined in a TOML configuration",
        add_help=False,
        epilog="Example: doteki -c config.toml -i README.md",
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="Print help",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=version("doteki"),
        help="Print version",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="doteki.toml",
        help="Path to the TOML configuration file. Default: doteki.toml",
    )
    parser.add_argument(
        "-i",
        "--input",
        default="README.md",
        help="Path to the README file. Default: README.md",
    )
    return parser.parse_args()


def exit_if_file_missing(file_path: str) -> None:
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        sys.exit(1)


def load_config(config_path: str) -> dict[str, Any]:
    exit_if_file_missing(config_path)
    try:
        with open(config_path, "rb") as config_file:
            return tomllib.load(config_file)
    except tomllib.TOMLDecodeError as e:
        logging.error(f"Error parsing TOML file: {e}")
        sys.exit(1)


def process_sections(global_config: dict[str, Any], readme_path: str) -> None:
    for section, section_settings in global_config["sections"].items():
        section_context = SectionContext(section, section_settings, readme_path)
        update_readme_content(section_context, global_config)


class SectionContext:
    def __init__(
        self,
        name: str,
        settings: dict[str, Any],
        readme_path: str,
    ):
        self.name: str = name
        self.settings: dict[str, Any] = settings
        self.readme_path: str = readme_path


def update_readme_content(
    section_context: SectionContext, global_config: dict[str, Any]
) -> None:
    section = section_context.name
    plugin_name = section_context.settings.get("plugin")
    if not plugin_name:
        logging.error(f"No plugin specified for section '{section}'")
        return
    inline = section_context.settings.get("inline", False)
    readme_content = read_file_content(section_context.readme_path)
    marker_format = global_config.get("marker_format", DEFAULT_MARKER_FORMAT)
    section_indices = find_section_indices(readme_content, section, marker_format)

    for start_index, end_index in reversed(section_indices):
        # Run the plugin in a logging context that includes the plugin name in the logs.
        with plugin_logging_context(plugin_name):
            new_content = get_plugin_output(plugin_name, section_context.settings)
        if new_content is None:
            logging.error(
                f"No content returned by plugin '{plugin_name}' for section '{section}'"
            )
            continue
        readme_content = replace_section_content(
            readme_content, new_content, start_index, end_index, inline
        )

    write_file_content(section_context.readme_path, readme_content)


def read_file_content(filepath: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    except IOError as e:
        logging.error(f"An error occurred while reading {filepath}: {e}")
        return ""


def find_section_indices(content: str, section: str, marker_format: str) -> list[tuple]:
    start_marker = re.escape(marker_format.format(name=section, position="start"))
    end_marker = re.escape(marker_format.format(name=section, position="end"))
    start_indices = [m.end() for m in re.finditer(start_marker, content)]
    end_indices = [m.start() for m in re.finditer(end_marker, content)]
    if not start_indices and not end_indices:
        logging.error(f"No markers found for section '{section}'")
        return []
    elif len(start_indices) != len(end_indices):
        logging.error(f"Mismatched markers for section '{section}'")
        return []
    return list(zip(start_indices, end_indices))


@contextlib.contextmanager
def plugin_logging_context(plugin_name: str):
    original_formatter = logging.getLogger().handlers[0].formatter
    new_format = f"[{plugin_name}] %(levelname)s: %(message)s"
    logging.getLogger().handlers[0].setFormatter(logging.Formatter(new_format))

    try:
        yield
    finally:
        # Revert to the original logging format.
        logging.getLogger().handlers[0].setFormatter(original_formatter)


def get_plugin_output(plugin_name: str, settings: dict[str, Any]) -> str | None:
    try:
        plugin_module = importlib.import_module(f"doteki.plugins.{plugin_name}")
        plugin_output = plugin_module.run(settings)
        if plugin_output is not None:
            return format_plugin_output(plugin_output, settings)

    except ImportError as e:
        logging.error(
            f"Missing dependency for plugin '{plugin_name}': {e}. Try running 'pip install doteki[{plugin_name}]'"
        )
    except AttributeError:
        logging.error(f"Plugin '{plugin_name}' does not have a 'run' function")
    except Exception as e:
        logging.error(f"An error occurred in plugin '{plugin_name}': {e}")
    return None


def format_bullet_list(output_list):
    if not output_list:
        return ""
    return "- " + "\n- ".join(output_list)


def format_numbered_list(output_list):
    return "\n".join(f"{i+1}. {item}" for i, item in enumerate(output_list))


def format_comma_and(output_list):
    if len(output_list) > 1:
        return ", ".join(output_list[:-1]) + ", and " + output_list[-1]
    return output_list[0] if output_list else ""


def format_space(output_list):
    return " ".join(output_list)


def format_glue(output_list):
    return "".join(output_list)


preset_functions = {
    "bullet_list": format_bullet_list,
    "numbered_list": format_numbered_list,
    "comma_and": format_comma_and,
    "space": format_space,
    "glue": format_glue,
}


def format_plugin_output(plugin_output: Any, settings: dict[str, Any]) -> str:
    prepend_text = settings.get("prepend_text", "")
    append_text = settings.get("append_text", "")
    preset = settings.get("preset", None)
    if isinstance(plugin_output, list):
        plugin_output = list(map(str, plugin_output))
        format_function = preset_functions.get(preset, format_bullet_list)
        formatted_output = format_function(plugin_output)
    else:
        formatted_output = str(plugin_output)
    return f"{prepend_text}{formatted_output}{append_text}"


def replace_section_content(
    original_content: str,
    new_content: str,
    start_index: int,
    end_index: int,
    inline: bool,
) -> str:
    if not inline:
        new_content = "\n" + new_content + "\n"
    updated_content = (
        original_content[:start_index] + new_content + original_content[end_index:]
    )
    return updated_content


def write_file_content(filepath: str, content: str) -> None:
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
    except IOError as e:
        logging.error(f"An error occurred while writing to {filepath}: {e}")


def insert_credits(global_config: dict[str, Any], readme_path: str) -> None:
    credits = global_config.get("credits", DEFAULT_CREDITS)
    readme_content = read_file_content(readme_path)
    if credits in read_file_content(readme_path):
        return
    write_file_content(readme_path, readme_content + "\n" + credits + "\n")


if __name__ == "__main__":
    main()  # pragma: no cover
