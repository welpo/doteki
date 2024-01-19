# General configuration

The settings for the main application go under the main (unnamed) TOML section:

```toml title="doteki.toml"
marker_format = "<!-- {name} {position} -->"
credits = '<a href="https://doteki.org"><img src="https://img.shields.io/badge/powered_by-d%C5%8Dteki-0?style=flat-square&labelColor=202b2d&color=5E936C" align="right" alt="Powered by dōteki"></a>'

# The main section ends here. The first section starts below.
[sections.last_updated]
```

## Marker format

The marker format is used to find the start and end markers in the file. The default format is:

```toml
marker_format = "<!-- {name} {position} -->"
```

This means sections will be found by looking for markers like this:

```md
<!-- blog start -->
<!-- blog end -->
```

Any string can be used as a marker, as long as it contains the `{name}` and `{position}` placeholders.

`{name}` will be replaced with the name of the section as defined in `doteki.toml`. This means `sections.blog` and `sections.BLOG` are different sections.

`{position}` will be replaced with either `start` or `end`, always in lowercase. Thus, `<!-- blog START -->` will not be recognised as a marker.

## Credits

By default, the processed `README.md` contains a small badge on the bottom right linking to the dōteki website:

<a href="https://doteki.org">
    <img alt="Powered by dōteki" src="https://img.shields.io/badge/powered_by-d%C5%8Dteki-0?style=flat-square&labelColor=202b2d&color=5E936C"></img>
</a>

<br></br>

You can configure this through the `credits` variable, which defaults to:

```toml
credits = '<a href="https://doteki.org"><img alt="Powered by dōteki" src="https://img.shields.io/badge/powered_by-d%C5%8Dteki-0?style=flat-square&labelColor=202b2d&color=5E936C" align="right"></a>'
```

If you'd like to simply add an invisible HTML comment, you could set it to:

```toml
credits = "<!-- Powered by https://doteki.org -->"
```

You can also disable them entirely by setting `credits = ""`.
