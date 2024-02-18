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
ascii_text = "hello"
font = "isometric1"
```

This will render the following:

```text
      ___           ___           ___       ___       ___     
     /\__\         /\  \         /\__\     /\__\     /\  \    
    /:/  /        /::\  \       /:/  /    /:/  /    /::\  \   
   /:/__/        /:/\:\  \     /:/  /    /:/  /    /:/\:\  \  
  /::\  \ ___   /::\~\:\  \   /:/  /    /:/  /    /:/  \:\  \ 
 /:/\:\  /\__\ /:/\:\ \:\__\ /:/__/    /:/__/    /:/__/ \:\__\
 \/__\:\/:/  / \:\~\:\ \/__/ \:\  \    \:\  \    \:\  \ /:/  /
      \::/  /   \:\ \:\__\    \:\  \    \:\  \    \:\  /:/  / 
      /:/  /     \:\ \/__/     \:\  \    \:\  \    \:\/:/  /  
     /:/  /       \:\__\        \:\__\    \:\__\    \::/  /   
     \/__/         \/__/         \/__/     \/__/     \/__/
```

## Frequently Asked Questions

### Where can I find a list of available fonts?

Check the [FIGlet official site](http://www.figlet.org/examples.html) to explore the available fonts.
