# FIGlet Plugin

Display text with customizable ASCII art using FIGlet fonts. If no font is provided, it defaults to the standard output. Useful for adding decorative displays in your documents or applications.

## Configuration

The FIGlet plugin can be configured with the following parameters:

- `text`: Text to be rendered in ASCII font.
- `font`: Specify the FIGlet font to use for rendering the text. Default is standard ASCII font.

## Usage

Here's an example with a custom font:

```toml title="doteki.toml"
[sections.ascii_art]
plugin = "figlet"
ascii_text = "text"
font = "larry3d"
```

This configuration will render the following:

```text
 __                   __      
/\ \__               /\ \__   
\ \ ,_\    __    ____\ \ ,_\  
 \ \ \/  /'__`\ /',__\\ \ \/  
  \ \ \_/\  __//\__, `\\ \ \_ 
   \ \__\ \____\/\____/ \ \__\
    \/__/\/____/\/___/   \/__/
```

## Frequently Asked Questions

### Where can I find a list of available fonts?

Check the [FIGlet official site](http://www.figlet.org/examples.html) to explore the available fonts.
