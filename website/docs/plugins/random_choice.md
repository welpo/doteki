# Random Choice Plugin

Return a random element from a list. Display a random quote, fact, emoji, or any other item from a predefined list.

## Configuration

The Random Choice plugin requires the following setting:

- `options`: A list of elements from which the plugin will randomly select. Elements can be strings like quotes, facts, emojis, etc.
- `n`: The number of elements to return. Default: `1`.
- `with_replacement`: Whether elements can be selected more than once. Only applies when `n` is greater than 1. Default: `false`.

## Usage

To use the Random Choice plugin, define a section in your `doteki.toml` file and provide a list of options. Here's a basic example:

```toml title="doteki.toml"
[sections.random_quote]
plugin = "random_choice"
options = [
    "I came to realize, clearly, that mind is no other than mountains and rivers and the great wide earth, the sun and the moon and the stars. — Dōgen Zenji",
    "Haven is a distance, not a place. - Carissa's Wierd",
    "This is my last message to you: in sorrow, seek happiness. - Fyodor Dostoevsky",
]
```

The plugin's output will be a randomly selected quote. For example:

```md
This is my last message to you: in sorrow, seek happiness. - Fyodor Dostoevsky
```

## Advanced usage

Here's an example using `n` > 1 and replacement enabled:

```toml title="doteki.toml"
[sections.garden]
plugin = "random_choice"
options = [
    "🌲", "🌳", "🌴", "🌱", "🍃", "🍂", "🌿",
    "🪻", "🍄", "🌷", "🌻", "🌺", "🎋", "☘️"
]
n = 10
with_replacement = true
preset = "glue"
```

The preset `glue` joins the selected items with no separator. One possible output:

```md
🌲🌺☘️🍄🌲🌴🌺🎋🍄🌺
```

Since `with_replacement` is `true`, the same emoji can appear more than once.
