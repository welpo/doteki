# Plugin Configuration

## Common configuration

All sections allow the following configuration options:

| Option | Description | Example |
| --- | --- | --- |
| `plugin` | The plugin to use for the section. | `plugin = "current_date"` |
| `prepend_text` | Text shown before whatever the plugin returns. | `prepend_text = "Last update: "` |
| `append_text` | Text shown at the end of the section. | `append_text = "."`|
| `inline` | Whether to render the plugin's output inline or as a block. Default: `false` | `inline = true` |
| `preset` | A predefined set of configuration options. Defaults to `bullet_list` when a plugin returns more than one item. See below for more options. | `preset = "bullet_list"` |

In the `prepend_text` and `append_text` fields, `\n` will be replaced with a newline character, and `\t` with a tab character, but only when they're inside double quotes (`"`). Single quotes (`'`) will treat them literal characters.

## Presets

### Bullet list (`bullet_list`)

The **default** preset when plugins return a list. Items are rendered as a bullet point list:

- Item 1
- Item 2
- Item 3

### Numbered list (`numbered_list`)

Renders elements as a numbered list:

1. Item 1
2. Item 2
3. Item 3

### Comma separated with "and" (`comma_and`)

Each item is rendered as a comma separated list, with "and" before the last item:

Item 1, Item 2, and Item 3

### Space separated (`space`)

Elements are joined together with a space:

Item 1 Item 2 Item 3

### Glue (`glue`)

Items are joined together with no separator:

Item 1Item 2Item 3

## Example

With a `README.md` like this:

```md
<!-- last_updated start --><!-- last_updated end -->
```

And a `doteki.toml` config with the example values from above:

```toml title="doteki.toml"
[sections.last_updated]
plugin = "current_date"
prepend_text = "Last updated on "
append_text = "."
inline = true
format = "%A, %d %B %Y"
```

dōteki would place this between the markers in `README.md`:

```md
Last updated on Wednesday, 21 October 2015.
```

You could get the same final output without `prepend_text` and `append_text`, by having this in your `README.md`:

```md
Last updated on <!-- last_updated start --><!-- last_updated end -->.
```

If you had `inline = false`, the output would be:

```md
Last updated on <!-- last_updated start -->
Wednesday, 21 October 2015
<!-- last_updated end -->.
```

which is probably not what you want.

## Specific configuration

Each plugin can have its own configuration options. See the plugin's page for more information. [Click to see the list of plugins](/docs/category/plugins).

## Environment variables

If a plugin is asking you to set an environment variable, it's because it needs to access sensitive information, such as an API key. If you added this information to `doteki.toml`, it would be visible to anyone who can see your repository.

### GitHub Action

If you're using the [GitHub Action](https://github.com/welpo/doteki-action), you can set secrets in your repository settings.

On your profile repository, go to the "Settings" tab and click on "Secrets and variables", then "Actions".

There you can create a new repository secret, say, "lastfm", and add the value for the variable there:

![Creating a secret](https://cdn.jsdelivr.net/gh/welpo/doteki-action@main/assets/secret.png)

Finally, in your workflow file, add a line at the end of the `steps` section, inside `env`:

```yaml
env:
  DOTEKI_LASTFM_API_KEY: ${{ secrets.lastfm }}
```

**Note**: The string on the left side is the name of the environment variable that the plugin expects. `secrets.<name>` must match the name of the secret you created.

### Running locally

Setting an environment variable in your shell will make it available to dōteki:

```bash
env DOTEKI_LASTFM_API_KEY="your-lastfm-api-key" doteki
```
