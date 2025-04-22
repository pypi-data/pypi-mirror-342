"""
Tests for the core functionality of pycommentcleaner.
"""

import os
import tempfile
from pathlib import Path

import pytest

from pycommentcleaner.core import clean_code, clean_file


class TestCleanCode:
    """Test cases for the clean_code function."""

    def test_basic_comment_removal(self):
        """Test removing basic comments."""
        code = "x = 1  # This is a comment"
        expected = "x = 1  "
        assert clean_code(code) == expected

    def test_standalone_comment_removal(self):
        """Test removing standalone comments."""
        code = "# This is a standalone comment\nx = 1"
        expected = " \nx = 1"
        assert clean_code(code) == expected

    def test_multiline_comment_removal(self):
        """Test removing comments across multiple lines."""
        code = "x = 1  # Comment 1\ny = 2  # Comment 2"
        expected = "x = 1  \ny = 2  "
        assert clean_code(code) == expected

    def test_comment_in_string(self):
        """Test that comments inside strings are preserved."""
        code = 'print("This # is not a comment")'
        expected = 'print("This # is not a comment")'
        assert clean_code(code) == expected

    def test_comment_in_docstring(self):
        """Test that comments inside docstrings are preserved."""
        code = '"""This is a docstring\n# This is not a comment\n"""\nx = 1'
        expected = '"""This is a docstring\n# This is not a comment\n"""\nx = 1'
        assert clean_code(code) == expected

    def test_comment_in_multiline_string(self):
        """Test that comments inside multiline strings are preserved."""
        code = "'''\nThis is a multiline string\n# This is not a comment\n'''\nx = 1"
        expected = "'''\nThis is a multiline string\n# This is not a comment\n'''\nx = 1"
        assert clean_code(code) == expected

    def test_empty_code(self):
        """Test handling empty code."""
        code = ""
        expected = ""
        assert clean_code(code) == expected

    def test_code_with_only_comments(self):
        """Test handling code with only comments."""
        code = "# Comment 1\n# Comment 2\n# Comment 3"
        expected = " \n \n "
        assert clean_code(code) == expected

    def test_code_with_escaped_quotes(self):
        """Test handling code with escaped quotes."""
        code = 'x = "This is a \\"quoted\\" string with # symbol"  # Comment'
        expected = 'x = "This is a \\"quoted\\" string with # symbol"  '
        assert clean_code(code) == expected

    def test_syntax_error_handling(self):
        """Test handling code with syntax errors."""
        # Code with syntax error (unclosed string)
        code = 'x = "unclosed string  # Comment'
        # Should return the original code
        assert clean_code(code) == code


class TestCleanFile:
    """Test cases for the clean_file function."""

    def test_file_cleaning(self):
        """Test cleaning a file and saving the result."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test file
            file_path = Path(temp_dir) / "test.py"
            with open(file_path, "w") as f:
                f.write("x = 1  # Comment\n# Another comment\ny = 2")
            
            # Clean the file
            success, _ = clean_file(file_path)
            
            # Check that the operation was successful
            assert success
            
            # Check that the output file was created
            output_path = Path(temp_dir) / "test_cleaned.py"
            assert output_path.exists()
            
            # Check the content of the output file
            with open(output_path, "r") as f:
                content = f.read()
            
            assert content == "x = 1  \n \ny = 2"

    def test_file_cleaning_with_custom_output(self):
        """Test cleaning a file with a custom output path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test file
            file_path = Path(temp_dir) / "test.py"
            with open(file_path, "w") as f:
                f.write("x = 1  # Comment")
            
            # Create a custom output path
            output_path = Path(temp_dir) / "custom_output.py"
            
            # Clean the file
            success, _ = clean_file(file_path, output_path)
            
            # Check that the operation was successful
            assert success
            
            # Check that the output file was created
            assert output_path.exists()
            
            # Check the content of the output file
            with open(output_path, "r") as f:
                content = f.read()
            
            assert content == "x = 1  "

    def test_nonexistent_file(self):
        """Test handling a nonexistent file."""
        file_path = Path("nonexistent_file.py")
        
        # Try to clean a nonexistent file
        success, _ = clean_file(file_path)
        
        # Check that the operation failed
        assert not success

    def test_non_python_file(self):
        """Test handling a non-Python file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test file with a non-Python extension
            file_path = Path(temp_dir) / "test.txt"
            with open(file_path, "w") as f:
                f.write("x = 1  # Comment")
            
            # Try to clean a non-Python file
            success, _ = clean_file(file_path)
            
            # Check that the operation failed
            assert not success