import pytest
import os
import tempfile
from md2html.converter import markdown_to_html, markdown_file_to_html

def test_basic_text():
    """Test basic text conversion"""
    markdown = "Hello, World!"
    html = markdown_to_html(markdown)
    assert "<p>Hello, World!</p>" in html
    assert "katex" in html.lower()

def test_headers():
    """Test header conversion"""
    markdown = "# Header 1\n## Header 2\n### Header 3"
    html = markdown_to_html(markdown)
    assert '<h1 id="header-1">Header 1</h1>' in html
    assert '<h2 id="header-2">Header 2</h2>' in html
    assert '<h3 id="header-3">Header 3</h3>' in html
    assert "katex" in html.lower()

def test_bold_and_italic():
    """Test bold and italic text conversion"""
    markdown = "**bold** and *italic*"
    html = markdown_to_html(markdown)
    assert "<strong>bold</strong>" in html
    assert "<em>italic</em>" in html
    assert "katex" in html.lower()

def test_lists():
    """Test unordered and ordered lists"""
    markdown = "- Item 1\n- Item 2\n\n1. First\n2. Second"
    html = markdown_to_html(markdown)
    assert "<ul>" in html
    assert "<li>Item 1</li>" in html
    assert "<li>Item 2</li>" in html
    assert "<ol>" in html
    assert "<li>First</li>" in html
    assert "<li>Second</li>" in html
    assert "katex" in html.lower()

def test_links():
    """Test link conversion"""
    markdown = "[Google](https://www.google.com)"
    html = markdown_to_html(markdown)
    assert '<a href="https://www.google.com">Google</a>' in html
    assert "katex" in html.lower()

def test_images():
    """Test image conversion"""
    markdown = "![Alt text](image.jpg)"
    html = markdown_to_html(markdown)
    assert '<img alt="Alt text" src="image.jpg">' in html
    assert "katex" in html.lower()

def test_code_blocks():
    """Test code block conversion with language specification"""
    markdown = "```python\ndef hello():\n    print('Hello')\n```"
    html = markdown_to_html(markdown)
    assert '<pre><code' in html
    assert 'print' in html
    assert '</code></pre>' in html
    assert "highlight.js" in html.lower()

def test_code_blocks_with_cpp():
    """Test code block conversion with C++ code"""
    markdown = '''```cpp
namespace test {
    int main() {
        return 0;
    }
}
```'''
    html = markdown_to_html(markdown)
    assert '<pre><code' in html
    assert 'namespace' in html
    assert '</code></pre>' in html
    assert "highlight.js" in html.lower()

def test_code_blocks_no_language():
    """Test code block conversion without language specification"""
    markdown = "```\nplain text\n```"
    html = markdown_to_html(markdown)
    assert '<pre><code' in html
    assert 'plain text' in html
    assert '</code></pre>' in html
    assert "highlight.js" in html.lower()

def test_inline_code():
    """Test inline code conversion"""
    markdown = "Use the `print()` function"
    html = markdown_to_html(markdown)
    assert '<code>' in html
    assert 'print()' in html

def test_blockquotes():
    """Test blockquote conversion"""
    markdown = "> This is a quote"
    html = markdown_to_html(markdown)
    assert "<blockquote>" in html
    assert "This is a quote" in html
    assert "katex" in html.lower()

def test_horizontal_rule():
    """Test horizontal rule conversion"""
    markdown = "---"
    html = markdown_to_html(markdown)
    assert "<hr>" in html
    assert "katex" in html.lower()

def test_empty_input():
    """Test empty input handling"""
    html = markdown_to_html("")
    assert html.strip() != ""  # Template should still be rendered
    assert "katex" in html.lower()

def test_none_input():
    """Test None input handling"""
    with pytest.raises(ValueError):
        markdown_to_html(None)

def test_invalid_input():
    """Test invalid input handling"""
    with pytest.raises(ValueError):
        markdown_to_html(123)  # Non-string input

def test_markdown_file_to_html_string():
    """Test converting markdown file to HTML string"""
    with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as tmp:
        tmp.write(b"# Hello, World!")
        tmp.flush()
        
        html = markdown_file_to_html(tmp.name)
        assert '<h1 id="hello-world">Hello, World!</h1>' in html
        assert "katex" in html.lower()
        
        os.unlink(tmp.name)

def test_markdown_file_to_html_file():
    """Test converting markdown file to HTML file"""
    with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as md_file:
        md_file.write(b"# Hello, World!")
        md_file.flush()
        
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as html_file:
            html_file_path = html_file.name
            
        # Convert and save to file
        markdown_file_to_html(md_file.name, html_file_path)
        
        # Read the saved HTML
        with open(html_file_path, 'r') as f:
            html = f.read()
            
        assert '<h1 id="hello-world">Hello, World!</h1>' in html
        assert "katex" in html.lower()
        
        # Clean up
        os.unlink(md_file.name)
        os.unlink(html_file_path)

def test_markdown_file_not_found():
    """Test handling of non-existent markdown file"""
    with pytest.raises(FileNotFoundError):
        markdown_file_to_html("nonexistent.md")

def test_markdown_file_wrong_extension():
    """Test handling of file with wrong extension"""
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
        with pytest.raises(ValueError):
            markdown_file_to_html(tmp.name)
        os.unlink(tmp.name)

def test_output_file_extension_handling():
    """Test automatic .html extension addition"""
    with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as md_file:
        md_file.write(b"# Hello, World!")
        md_file.flush()
        
        with tempfile.NamedTemporaryFile(delete=False) as html_file:
            html_file_path = html_file.name
            
        # Convert and save to file without .html extension
        markdown_file_to_html(md_file.name, html_file_path)
        
        # Check that .html was added
        assert os.path.exists(f"{html_file_path}.html")
        
        # Clean up
        os.unlink(md_file.name)
        os.unlink(f"{html_file_path}.html")

def test_inline_math():
    """Test inline LaTeX math conversion"""
    markdown = "The quadratic formula is $x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$."
    html = markdown_to_html(markdown)
    assert "katex" in html.lower()
    assert "\\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}" in html

def test_block_math():
    """Test block LaTeX math conversion"""
    markdown = """The integral of a function is:
$$
\\int_{a}^{b} f(x) \\, dx = F(b) - F(a)
$$"""
    html = markdown_to_html(markdown)
    assert "katex" in html.lower()
    assert "$$" in html
    assert "integral of a function" in html
    assert 'display: true' in html.lower()  # Check for KaTeX display mode configuration

def test_math_with_text():
    """Test LaTeX math with surrounding text"""
    markdown = """
# Math Example

This is a paragraph with inline math: $E = mc^2$.

And here's a block equation:
$$
\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}
$$
"""
    html = markdown_to_html(markdown)
    assert "katex" in html.lower()
    assert "E = mc^2" in html
    assert "\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}" in html
    assert '<h1 id="math-example">Math Example</h1>' in html
    assert "This is a paragraph" in html
