---
sidebar_position: 2
---

# How to Write a Plugin

Plugins are the building blocks of dōteki. They are standalone Python modules that provide data to the main application.

What kind of data? Anything you'd like to showcase on your GitHub profile. Take a look at the [available plugins](/docs/category/plugins/) to see some examples.

:::tip
Before you start developing a plugin, [set up your development environment](/docs/developer-guide/).
:::

## General recommendations

- Set **sane defaults** for settings that allow it. For example, the `current_date` plugin uses the ISO standard (`"%Y-%m-%d"`) as the default `format`.
- Think of other users; aim for **flexibility**. For example, the `lastfm` plugin can display top artists, albums, tracks, or tags, even though the original use case was to display top artists.
- Follow the [**coding guidelines**](/docs/developer-guide/contributing#coding-guidelines).

## Plugin structure

**TL;DR**: Plugins must have a `run` function that returns a single item or a list of items. In case of an error, the plugin should log an appropriate message and return `None`.

### The `run` function

Plugins must have a `run` function. This is the entry point for the plugin and is called by the main application. The `run` function should adhere to the following signature:

```python
from typing import Any

def run(settings: dict[str, Any]) -> Any:
    # Plugin logic.
```

You can be more specific about the return types. For example, if your plugin only returns a string, a list of strings, you can use:

```python
from typing import Any

def run(settings: dict[str, Any]) -> str | list[str] | None:
```

We include `None` in the return type for [error handling](#error-handling).

Generally, you'll want to follow this second signature to have more control over the output.

Remember: GitHub readmes support Markdown, so the plugin can return Markdown-formatted strings for bold text, links, etc. See the [GitHub docs](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) to learn more about the supported Markdown syntax.

#### Arguments

The `run` function accepts a single argument: a dictionary containing the settings for the plugin.

#### Return values

The `run` function can return a single item or a list of items. These items will be rendered as strings. The main application will format the list.

In case of an error, the plugin must return `None` so dōteki skips the section.

:::tip
To render an empty section, return an empty string.
:::

### Other functions

Plugins may have other functions, but they will not be called by the main application.

For example, it's a good idea to have a `validate_settings` function to validate user settings. See the code of the [current_date plugin](https://github.com/welpo/doteki/blob/main/doteki/plugins/current_date.py) for a simple example.

## Error handling

In case of an error, the plugin should log an appropriate message using `logging` and return `None`:

```python
important_setting = settings.get("url")
if not important_setting:
    logging.error("No 'important_setting' provided for the Foo plugin")
    return None
```

You don't need to configure the logger; the main application takes care of that.

## Environment variables

If your plugin needs to access sensitive information, such as an API key, it must do so through environment variables. This is to avoid leaking the information in the configuration file.

The environment variable name must be `DOTEKI_<PLUGIN_NAME>_<SETTING_NAME>`. For example, the `lastfm` plugin uses `DOTEKI_LASTFM_API_KEY`.

Make sure you mask the environment variable in your logs. For example:

```py
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.RequestException as e:
    safe_error_message = str(e).replace(api_key, "HIDDEN_API_KEY")
    logging.error(f"Error fetching data: {safe_error_message}")
    return None
```

## Testing

Each plugin must have a corresponding test file in the `tests` directory. The filename must be `test_<plugin_name>.py`. For example, the `current_date` plugin has its tests in `tests/test_current_date.py`.

Write clear and concise tests, considering all edge cases you can think of.

To run all tests:

```bash
poetry run pytest
```

If you use VSCode, you might want to install the [Python Test Explorer](https://marketplace.visualstudio.com/items?itemName=LittleFoxTeam.vscode-python-test-adapter) extension.

### Code coverage

Plugins must have 80%+ code coverage. Aim for 100%, but don't let this stop you from contributing; do your best and reach out for help if needed. Do keep in mind functionality coverage (testing all features and edge cases) is more important than code coverage.

To generate a code coverage report, run:

```bash
poetry run pytest --cov=doteki
```

For VSCode users, the [Coverage Gutters](https://marketplace.visualstudio.com/items?itemName=ryanluker.vscode-coverage-gutters) extension can highlight lines not covered by tests. This extension needs a a coverage report; generate it with:

```bash
poetry run pytest --cov=doteki --cov-report xml
```

## Adding dependencies

dōteki uses [Poetry](https://python-poetry.org/) to manage dependencies. The `pyproject.toml` file contains all the dependencies, including development dependencies.

**All plugin dependencies must be marked as optional**.

If your plugin adds a dependency, you need to:

1. Add it to the `pyproject.toml` file. You can run `poetry add {dependency_name}` to do this.
2. Mark it as optional. Example:

   ```toml
   [tool.poetry.dependencies]
   pandas = {version = "^2.1.4", optional = true}
   ```

3. Add your plugin name with its dependencies to the `[tool.poetry.extras]` section. Example:

    ```toml
    [tool.poetry.extras]
    plugin_name = ["pandas"]
    ```

4. Update the `all` section in `[tool.poetry.extras]` to add the new dependencies, if needed:

    ```toml
    [tool.poetry.extras]
    all = ["requests", "feedparser", "pandas"]
    ```

## Documentation

Each plugin must have a Markdown file in the `website/docs/plugins` directory. The filename must match the name of the plugin. For example, the documentation for the `current_date` plugin can be found in `website/docs/plugins/current_date.md`.

This Markdown file must include:

- A description of the plugin's purpose.
- A list of dependencies.
- An explanation of all configuration options.
- Usage example(s).

Check out the [Feed Plugin Documentation](/docs/plugins/feed/) for an example.

Read more about the website and documentation [here](/docs/developer-guide/website).

## Example

The Pull Request to add the [Current Date plugin](/docs/plugins/current_date) would need to include:

- The [plugin code](https://github.com/welpo/doteki/blob/main/doteki/plugins/current_date.py) in `doteki/plugins/current_date.py`.
- The [tests](https://github.com/welpo/doteki/blob/main/tests/test_current_date.py) in `tests/plugins/test_current_date.py`.
- The [documentation](https://github.com/welpo/doteki/blob/main/website/docs/plugins/current_date.md) in `website/docs/plugins/current_date.md`. (See the the page live [here](/docs/plugins/current_date/).)
- Any plugin dependency changes in `pyproject.toml`. (No changes in this case.)

## Questions?

If something is not clear, or you have any questions, don't hesitate to reach out via the [issue tracker](https://github.com/welpo/doteki/issues), [discussions](https://github.com/welpo/doteki/discussions), or [email](mailto:osc@osc.garden?subject=[GitHub]%20dōteki).
