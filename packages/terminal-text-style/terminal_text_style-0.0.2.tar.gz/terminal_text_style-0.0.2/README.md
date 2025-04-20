# terminal-text-style

**terminal-text-style** is a lightweight Python package designed to simplify the process of styling terminal output with colors, background highlights, and text effects.

This project aims to help beginners and the broader community easily improve the readability and visual appeal of terminal outputs using clean and intuitive syntax.

## Features

- Apply text colors (e.g. red, green, blue)  
- Add background colors  
- Use text styles like bold, underline, and reverse  
- Simple functions — no complex ANSI codes required  
- Easy to integrate into any CLI or script  

## Installation

You can install the package via [PyPI](https://pypi.org/project/terminal-text-style/):

```bash
pip install terminal-text-style
```

## Example

```python
from terminal_text_style import color_text

# message in bold
print(color_text(type='bold', message='Abacaxi com goiaba'))

# text in red
print(color_text(text='red', message='Abacaxi com goiaba'))

# yellow background
print(color_text(back='yellow', message='Abacaxi com goiaba'))

# strike message with green background
print(color_text(type='strike', back='green', message='Abacaxi com goiaba'))

# bold message with yellow text
print(color_text(type='bold', text='yellow', message='Abacaxi com goiaba'))

# red background, withe text
print(color_text(back='red', text='white', message='Abacaxi com goiaba'))

# bold message with magenta color and black background
print(color_text(text='magenta', type='bold', back='black', message='Abacaxi com goiaba'))
```

## Compatibility

This package is written in pure Python and should work on most systems that support ANSI escape codes (Linux, macOS, and some terminals on Windows).

## License

MIT License