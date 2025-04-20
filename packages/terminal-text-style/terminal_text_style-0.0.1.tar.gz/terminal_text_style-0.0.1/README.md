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

Coming soon on PyPI!  
For now, you can clone the repository and use it locally:

```bash
git clone https://github.com/Victor-f-Paiva/terminal-text-style.git
```

## Example

```python
from terminal_text_style import style as s

print(s.color_text(type='bold', message='Abacaxi com goiaba'))
print(s.color_text(text='red', message='Abacaxi com goiaba'))
print(s.color_text(back='yellow', message='Abacaxi com goiaba'))
print(s.color_text(type='strike', back='green', message='Abacaxi com goiaba'))
print(s.color_text(type='bold', text='yellow', message='Abacaxi com goiaba'))
print(s.color_text(back='red', text='white', message='Abacaxi com goiaba'))
print(s.color_text(text='magenta', type='bold', back='black', message='Abacaxi com goiaba'))
```

## Compatibility

This package is written in pure Python and should work on most systems that support ANSI escape codes (Linux, macOS, and some terminals on Windows).

## License

MIT License