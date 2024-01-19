import logging
import random
from typing import Any

DEFAULT_N = 1
DEFAULT_WITH_REPLACEMENT = False


def run(settings: dict[str, Any]) -> str | list[str] | None:
    if not validate_settings(settings):
        return None
    options = settings.get("options", [])
    n = settings.get("n", DEFAULT_N)
    with_replacement = settings.get("with_replacement", DEFAULT_WITH_REPLACEMENT)

    if n == 1:
        return str(random.choice(options))
    if with_replacement:
        return [random.choice(options) for _ in range(n)]
    else:
        return random.sample(options, n)


def validate_settings(settings: dict[str, Any]) -> bool:
    errors = []

    options = settings.get("options", [])
    if not options:
        errors.append("No options provided for the Random Choice plugin")
    elif not isinstance(options, list):
        errors.append("Invalid type for 'options'. Expected list")

    n = settings.get("n")
    if n is not None:
        if not isinstance(n, int) or n < 1:
            errors.append("Invalid value for 'n'. Expected a positive int")
        elif not settings.get("with_replacement", False) and len(options) < n:
            errors.append(
                "'n' is greater than the number of options and `with_replacement` is false"
            )

    with_replacement = settings.get("with_replacement")
    if with_replacement is not None and not isinstance(with_replacement, bool):
        errors.append("Invalid type for 'with_replacement'. Expected bool")

    if errors:
        for error in errors:
            logging.error(error)
        return False

    return True
