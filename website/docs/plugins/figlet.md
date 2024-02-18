# FIGlet Plugin

Display text with customizable ASCII art using FIGlet fonts.

## Configuration

The FIGlet plugin can be configured with the following parameters:

- `text`: Text to be rendered in ASCII font.
- `font`: FIGlet font to use. Defaults to `standard`.

## Usage

Here's an example configuration:

```toml title="doteki.toml"
[sections.ascii_art]
plugin = "figlet"
ascii_text = "text"
font = "larry3d"
```

This will render the following:

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
