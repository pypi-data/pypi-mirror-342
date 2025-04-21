# Markdown to HTML Converter with Math Support

A Python package that converts markdown text to HTML with LaTeX math support and beautiful styling.

## Installation

```bash
pip install md2html-math
```

## Usage

### Command Line Interface

```bash
# Convert a markdown file to HTML (output will be in the same directory)
md2html-math /path/to/input.md

# Convert a markdown file to HTML with custom output path
md2html-math /path/to/input.md --output /path/to/output.html
# or
md2html-math /path/to/input.md -o /path/to/output.html
```

### Python API

#### Converting Markdown Strings

```python
from md2html.converter import markdown_to_html

# Basic usage
markdown_text = "# Hello, World!"
html = markdown_to_html(markdown_text)
print(html)
# Output: <h1>Hello, World!</h1>

# With LaTeX math
markdown_text = """
# Math Example

Inline math: $E = mc^2$

Block math:
$$
\\frac{n!}{k!(n-k)!} = \\binom{n}{k}
$$
"""

html = markdown_to_html(markdown_text)
print(html)
```

#### Converting Markdown Files

```python
from md2html.converter import markdown_file_to_html

# Convert markdown file to HTML string
html = markdown_file_to_html("input.md")
print(html)

# Convert markdown file and save to HTML file
markdown_file_to_html("input.md", "output.html")  # Will create output.html
markdown_file_to_html("input.md", "output")       # Will create output.html
```

## Features

- Beautiful, responsive HTML output with modern styling
- LaTeX math support:
  - Inline math using `$...$` or `\(...\)`
  - Block math using `$$...$$` or `\[...\]`
  - Powered by KaTeX for fast rendering
- Markdown features:
  - Headers (#, ##, ###, etc.)
  - Bold and italic text
  - Lists (ordered and unordered)
  - Links and images
  - Code blocks with syntax highlighting
  - Blockquotes
  - Horizontal rules
  - Tables
  - Footnotes
  - Table of contents
  - And more!
- File conversion support:
  - Convert markdown files to HTML strings
  - Save HTML output to files
  - Automatic .html extension handling
  - UTF-8 encoding support
- Command line interface:
  - Convert files from the command line
  - Automatic output file generation
  - Custom output path support
  - Error handling and user feedback

## Math Examples

### Inline Math
```markdown
The quadratic formula is $x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$.
```

### Block Math
```markdown
The integral of a function is:
$$
\\int_{a}^{b} f(x) \\, dx = F(b) - F(a)
$$
```

## Development

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/md2html-math.git
cd md2html-math

# Create and activate a virtual environment
conda create -n md2html-math python=3.11
conda activate md2html-math

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## License

MIT License 