import argparse
import sys
import os
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
        # If output file is not specified, use input file name with .html extension
        output_file = args.output
        if output_file is None:
            output_file = os.path.splitext(args.input_file)[0] + '.html'
        elif not output_file.lower().endswith('.html'):
            output_file = f"{output_file}.html"
            
        markdown_file_to_html(args.input_file, output_file)
        print(f"Successfully converted {args.input_file} to {output_file}")
        return 0
    except FileNotFoundError as e:
        print(f"Error: Input file not found: {args.input_file}")
        return 1
    except ValueError as e:
        print(f"Error: {str(e)}")
        return 1
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 