import argparse
import sys
from .converter import markdown_file_to_html

def main():
    """Command line interface for markdown to HTML conversion."""
    parser = argparse.ArgumentParser(
        description="Convert markdown files to HTML with LaTeX math support"
    )
    parser.add_argument(
        "input_file",
        help="Path to the markdown file to convert"
    )
    parser.add_argument(
        "-o", "--output",
        help="Path where to save the HTML output (default: same as input with .html extension)"
    )
    
    args = parser.parse_args()
    
    try:
        markdown_file_to_html(args.input_file, args.output)
        print(f"Successfully converted {args.input_file} to HTML")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 