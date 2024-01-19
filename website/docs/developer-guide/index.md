---
sidebar_position: 5
title: Developer Guide
---

## Initial setup

To get started, you'll need to set up your development environment:

1. [Install Poetry](https://python-poetry.org/docs/#installation):

  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```

2. Set up the development environment (run from the project root):

  ```bash
  poetry install --all-extras  # Remove --all-extras to ignore plugin dependencies.
  ```

3. Start the poetry shell:

  ```bash
  poetry shell
  ```

Now you can run `doteki` within the shell:

```bash
doteki --help
```

The `doteki` command will be available within the `poetry shell` and is linked to the project's source code. Any changes to the code will be reflected in the command.

## Useful commands

### Running tests

```bash
poetry run pytest
```

### Checking code coverage

```bash
poetry run pytest --cov=doteki
```

### Checking types

```bash
poetry run mypy doteki
```

### Formatting code

dōteki uses [Black](https://github.com/psf/black) to format the code. To format a file or directory:

```bash
poetry run black {source file or directory}
```

## Further reading

- [Contributing Guidelines](contributing/).
- [Developing Plugins](plugin-standard/).
- [Website & Documentation](website/).

## Questions?

If you have any questions, don't hesitate to reach out via the [issue tracker](https://github.com/welpo/doteki/issues) or [email](mailto:osc@osc.garden?subject=[GitHub]%20dōteki).
