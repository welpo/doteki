# Figlet Plugin

Display text with customizable ASCII art using Figlet fonts. If no font is provided, it defaults to the standard output. Useful for adding decorative displays in your documents or applications.

## Configuration

The Figlet plugin can be configured with the following parameters:

- `text`: Text to be rendered in ASCII font.
- `font`: Specify the Figlet font to use for rendering the text. Default is standard ASCII font.

## Usage

Using a custom format and prepending and appending some text:

```toml title="doteki.toml"
[sections.ascii_art]
plugin = "figlet"
ascii_text = "text"
font = "standard"
```

dōteki would generate:

```md
 _            _
| |_ _____  _| |_
| __/ _ \ \/ / __|
| ||  __/>  <| |_
 \__\___/_/\_\\__|
```

## Frequently Asked Questions

### What are the available fonts?

Check the [FIGlet official site](http://www.figlet.org/#format-codes) to see several samples of available fonts.
