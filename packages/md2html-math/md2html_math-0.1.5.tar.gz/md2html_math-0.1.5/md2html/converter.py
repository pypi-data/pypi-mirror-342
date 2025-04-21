import markdown
from typing import Union
import os
from pathlib import Path
import jinja2
import re
import textwrap

def _get_template():
    """Get the Jinja2 template for HTML output."""
    template_dir = Path(__file__).parent / 'templates'
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(template_dir)),
        autoescape=True
    )
    return env.get_template('base.html')

def _preprocess_code_blocks(markdown_text: str) -> str:
    """
    Preprocess code blocks to ensure proper rendering.
    Handles both fenced code blocks (```) and inline code blocks (`).
    """
    # Fix triple backtick code blocks
    # This pattern matches triple backticks with optional language specification
    pattern = r'```(\w*)\n(.*?)```'
    
    def replace_code_block(match):
        lang = match.group(1) or 'plaintext'
        code = match.group(2)
        
        # Dedent the code block while preserving relative indentation
        code = textwrap.dedent(code)
        
        # Ensure each line is properly indented relative to the first line
        lines = code.split('\n')
        if lines:
            # Find the minimum indentation level (excluding empty lines)
            min_indent = float('inf')
            for line in lines:
                if line.strip():  # Skip empty lines
                    indent = len(line) - len(line.lstrip())
                    min_indent = min(min_indent, indent)
            min_indent = 0 if min_indent == float('inf') else min_indent
            
            # Adjust indentation while preserving relative levels
            processed_lines = []
            for line in lines:
                if line.strip():  # If line is not empty
                    # Remove original indentation and add new base indentation
                    line_content = line[min_indent:] if min_indent < len(line) else line
                    processed_lines.append(line_content)
                else:
                    processed_lines.append(line)  # Keep empty lines as is
            
            code = '\n'.join(processed_lines)
        
        # Add consistent indentation for the entire block
        code = textwrap.indent(code, '    ')
        
        return f'\n```{lang}\n{code}\n```\n'
    
    # Replace all code blocks while preserving language info
    markdown_text = re.sub(pattern, replace_code_block, markdown_text, flags=re.DOTALL)
    
    return markdown_text

def markdown_to_html(markdown_text: Union[str, None]) -> str:
    """
    Convert a markdown string to HTML.
    
    Args:
        markdown_text (Union[str, None]): The markdown text to convert. Can be None or empty string.
        
    Returns:
        str: The converted HTML string.
        
    Raises:
        ValueError: If the input is None or not a string.
    """
    if markdown_text is None:
        raise ValueError("Input cannot be None")
    
    if not isinstance(markdown_text, str):
        raise ValueError("Input must be a string")
    
    # Preprocess code blocks
    markdown_text = _preprocess_code_blocks(markdown_text)
    
    # Configure markdown extensions for better HTML output
    extensions = [
        'extra',  # Adds support for tables, fenced code blocks, etc.
        'pymdownx.superfences',  # Better fenced code block support
        'codehilite',  # Adds syntax highlighting to code blocks
        'tables',  # Better table support
        'nl2br',  # Convert newlines to <br> tags
        'sane_lists',  # Better list handling
        'footnotes',  # Footnote support
        'toc',  # Table of contents support
        'pymdownx.arithmatex',  # LaTeX math support
        'fenced_code',  # Explicit fenced code support
    ]
    
    # Configure extensions
    extension_configs = {
        'codehilite': {
            'css_class': 'hljs',
            'use_pygments': False,
            'noclasses': False,
            'guess_lang': False
        },
        'pymdownx.superfences': {
            'disable_indented_code_blocks': False,
            'preserve_tabs': True,
            'custom_fences': [
                {
                    'name': 'mermaid',
                    'class': 'mermaid',
                    'format': str
                }
            ]
        },
        'fenced_code': {
            'lang_prefix': 'language-'
        },
        'pymdownx.arithmatex': {
            'generic': True,
            'preview': False
        }
    }
    
    # Convert markdown to HTML with proper code block handling
    html = markdown.markdown(
        markdown_text,
        extensions=extensions,
        extension_configs=extension_configs,
        output_format='html5'
    )
    
    # Post-process code blocks to ensure proper formatting
    # Handle fenced code blocks with language specification
    html = re.sub(
        r'<pre><code\s+class="([^"]+)">(.*?)</code></pre>',
        lambda m: f'<pre><code class="{m.group(1)}">{m.group(2)}</code></pre>',
        html,
        flags=re.DOTALL
    )
    
    # Handle code blocks without language specification
    html = re.sub(
        r'<pre><code(?!\s+class=)(.*?)>(.*?)</code></pre>',
        lambda m: f'<pre><code class="language-plaintext">{m.group(2)}</code></pre>',
        html,
        flags=re.DOTALL
    )
    
    # Wrap in template
    template = _get_template()
    return template.render(
        title="Markdown Document",
        content=html
    )

def markdown_file_to_html(markdown_file: str, output_file: Union[str, None] = None) -> str:
    """
    Convert a markdown file to HTML and optionally save it to a file.
    
    Args:
        markdown_file (str): Path to the markdown file to convert.
        output_file (Union[str, None], optional): Path where to save the HTML output.
            If None, the output will be saved with the same name as input but .html extension.
            
    Returns:
        str: The converted HTML string if output_file is None, otherwise an empty string.
        
    Raises:
        FileNotFoundError: If the markdown file doesn't exist.
        ValueError: If the markdown file is not a .md file.
    """
    if not os.path.exists(markdown_file):
        raise FileNotFoundError(f"Markdown file not found: {markdown_file}")
    
    if not markdown_file.lower().endswith('.md'):
        raise ValueError("Input file must have a .md extension")
    
    # Read the markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_text = f.read()
    
    # Convert to HTML
    html = markdown_to_html(markdown_text)
    
    # If output file is not specified, use input file name with .html extension
    if output_file is None:
        output_file = os.path.splitext(markdown_file)[0] + '.html'
    elif not output_file.lower().endswith('.html'):
        output_file = f"{output_file}.html"
    
    # Save the HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return html
