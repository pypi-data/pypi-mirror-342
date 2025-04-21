import pytest
import os
import tempfile
from unittest.mock import patch
from md2html.cli import main

def test_cli_successful_conversion():
    """Test successful CLI conversion"""
    with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as md_file:
        md_file.write(b"# Hello, World!")
        md_file.flush()
        
        # Mock sys.argv
        with patch('sys.argv', ['md2html', md_file.name]):
            # Mock print to capture output
            with patch('builtins.print') as mock_print:
                result = main()
                
                # Check that conversion was successful
                assert result == 0
                
                # Check that output file was created
                output_file = os.path.splitext(md_file.name)[0] + '.html'
                assert os.path.exists(output_file)
                
                # Check that success message was printed
                mock_print.assert_called_with(
                    f"Successfully converted {md_file.name} to {output_file}"
                )
                
                # Clean up
                os.unlink(md_file.name)
                os.unlink(output_file)

def test_cli_custom_output():
    """Test CLI with custom output path"""
    with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as md_file:
        md_file.write(b"# Hello, World!")
        md_file.flush()
        
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as html_file:
            html_file_path = html_file.name
            
        # Mock sys.argv
        with patch('sys.argv', ['md2html', md_file.name, '--output', html_file_path]):
            # Mock print to capture output
            with patch('builtins.print') as mock_print:
                result = main()
                
                # Check that conversion was successful
                assert result == 0
                
                # Check that output file was created
                assert os.path.exists(html_file_path)
                
                # Check that success message was printed
                mock_print.assert_called_with(
                    f"Successfully converted {md_file.name} to {html_file_path}"
                )
                
                # Clean up
                os.unlink(md_file.name)
                os.unlink(html_file_path)

def test_cli_nonexistent_file():
    """Test CLI with non-existent input file"""
    # Mock sys.argv
    with patch('sys.argv', ['md2html', 'nonexistent.md']):
        # Mock print to capture output
        with patch('builtins.print') as mock_print:
            result = main()
            
            # Check that conversion failed
            assert result == 1
            
            # Check that error message was printed
            mock_print.assert_called_with(
                "Error: Input file not found: nonexistent.md"
            )

def test_cli_wrong_extension():
    """Test CLI with wrong file extension"""
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
        # Mock sys.argv
        with patch('sys.argv', ['md2html', tmp.name]):
            # Mock print to capture output
            with patch('builtins.print') as mock_print:
                result = main()
                
                # Check that conversion failed
                assert result == 1
                
                # Check that error message was printed
                mock_print.assert_called_with(
                    "Error: Input file must have a .md extension"
                )
                
                # Clean up
                os.unlink(tmp.name) 