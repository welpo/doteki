import pytest

from doteki.plugins.random_choice import run


def test_run():
    settings = {
        "options": ["a", "b", "c"],
    }
    result = run(settings)
    assert isinstance(result, str)
    assert result in settings["options"]


def test_empty_options(caplog):
    settings = {
        "options": [],
    }
    result = run(settings)
    assert result is None
    assert "No options provided for the Random Choice plugin" in caplog.text


def test_invalid_options(caplog):
    settings = {
        "options": "a",
    }
    result = run(settings)
    assert result is None
    assert "Invalid type for 'options'. Expected list" in caplog.text


def test_multiple_invalid_settings(caplog):
    settings = {
        "options": "a",
        "n": "1",
        "with_replacement": "False",
    }
    result = run(settings)
    assert result is None
    assert "Invalid type for 'options'. Expected list" in caplog.text
    assert "Invalid value for 'n'. Expected a positive int" in caplog.text
    assert "Invalid type for 'with_replacement'. Expected bool" in caplog.text


def test_n_greater_than_options(caplog):
    settings = {
        "options": ["a", "b", "c"],
        "n": 4,
    }
    result = run(settings)
    assert result is None
    assert "'n' is greater than the number of options" in caplog.text


def test_n_greater_than_options_with_replacement(caplog):
    settings = {
        "options": ["a", "b", "c"],
        "n": 4,
        "with_replacement": True,
    }
    result = run(settings)
    assert isinstance(result, list)
    assert len(result) == 4


def test_only_one_option():
    settings = {
        "options": ["a"],
    }
    result = run(settings)
    assert isinstance(result, str)
    assert result == "a"


@pytest.mark.parametrize("n", [-1, "1", 0, 1.5, "two"])
def test_invalid_n(n, caplog):
    settings = {
        "options": ["a", "b", "c"],
        "n": n,
    }
    result = run(settings)
    assert result is None
    assert "positive int" in caplog.text


def test_without_replacement():
    settings = {
        "options": ["a", "b", "c"],
        "n": 2,
        "with_replacement": False,
    }
    result = run(settings)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] in settings["options"]
    assert result[1] in settings["options"]
    assert result[0] != result[1]


def test_with_replacement():
    settings = {
        "options": ["heads", "tails"],
        "n": 1000,  # 1.87e−301 chance of failing.
        "with_replacement": True,
    }

    result = run(settings)
    assert isinstance(result, list)
    assert len(result) == 1000
    assert all(option in settings["options"] for option in result)
    assert "heads" in result, "No 'heads' in result. Boy, that's unlucky."
    assert "tails" in result, "No 'tails' in result. Impressive."


def test_n_equal_to_options_length_without_replacement():
    options = ["option1", "option2", "option3"]
    settings = {"options": options, "n": len(options), "with_replacement": False}
    result = run(settings)

    assert isinstance(result, list), "Expected a list"
    assert len(result) == len(
        options
    ), "Expected list length equal to number of options."
    assert set(result) == set(
        options
    ), "Expected all options to be present in the result."
