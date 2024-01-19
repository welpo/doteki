# Current Date Plugin

Get the current date formatted according to a specified format. If no format is provided, it defaults to the ISO date format ("YYYY-MM-DD"). Useful to display the last time a page was updated, for example.

## Configuration

The Current Date plugin can be configured with the following option:

- `format`: A string specifying the date format, following Python's `datetime` module format codes. The default format is "YYYY-MM-DD" (`%Y-%m-%d`).

## Usage

Using a custom format and prepending and appending some text:

```toml title="doteki.toml"
[sections.last_updated]
plugin = "current_date"
format = "%A, %d %B %Y"
prepend_text = "Last updated on "
append_text = "."
```

dōteki would generate:

```md
Last updated on Wednesday, 21 October 2015.
```

## Frequently Asked Questions

### What are the available date format codes?

Check the [Python documentation](https://docs.python.org/3/library/datetime.html#format-codes) to see all the datetime format codes.
