"""
Tests for the command-line interface of pycommentcleaner.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from pycommentcleaner.cli import main, parse_args


class TestParseArgs:
    """Test cases for the parse_args function."""

    def test_basic_args(self):
        """Test basic argument parsing."""
        args = parse_args(["file.py"])
        assert args.files == ["file.py"]
        assert args.output_dir is None
        assert args.verbose == 0

    def test_multiple_files(self):
        """Test parsing multiple file arguments."""
        args = parse_args(["file1.py", "file2.py", "file3.py"])
        assert args.files == ["file1.py", "file2.py", "file3.py"]

    def test_output_dir(self):
        """Test parsing output directory argument."""
        args = parse_args(["file.py", "--output-dir", "output"])
        assert args.files == ["file.py"]
        assert args.output_dir == "output"

    def test_verbose(self):
        """Test parsing verbose argument."""
        args = parse_args(["file.py", "-v"])
        assert args.verbose == 1
        
        args = parse_args(["file.py", "-vv"])
        assert args.verbose == 2
        
        args = parse_args(["file.py", "-vvv"])
        assert args.verbose == 3


class TestMain:
    """Test cases for the main function."""

    @patch("pycommentcleaner.cli.clean_file")
    def test_single_file(self, mock_clean_file):
        """Test processing a single file."""
        # Mock clean_file to return success
        mock_clean_file.return_value = (True, "Success message")
        
        # Call main with a single file
        exit_code = main(["file.py"])
        
        # Check that clean_file was called correctly
        mock_clean_file.assert_called_once()
        args, _ = mock_clean_file.call_args
        assert str(args[0]) == "file.py"
        
        # Check that the exit code is correct
        assert exit_code == 0

    @patch("pycommentcleaner.cli.clean_file")
    def test_single_file_failure(self, mock_clean_file):
        """Test processing a single file that fails."""
        # Mock clean_file to return failure
        mock_clean_file.return_value = (False, "Error message")
        
        # Call main with a single file
        exit_code = main(["file.py"])
        
        # Check that clean_file was called correctly
        mock_clean_file.assert_called_once()
        
        # Check that the exit code is correct
        assert exit_code == 1

    @patch("pycommentcleaner.cli.clean_files")
    def test_multiple_files(self, mock_clean_files):
        """Test processing multiple files."""
        # Mock clean_files to return success for all files
        mock_clean_files.return_value = [
            ("file1.py", True, "Success message 1"),
            ("file2.py", True, "Success message 2"),
        ]
        
        # Call main with multiple files
        exit_code = main(["file1.py", "file2.py"])
        
        # Check that clean_files was called correctly
        mock_clean_files.assert_called_once()
        
        # Check that the exit code is correct
        assert exit_code == 0

    @patch("pycommentcleaner.cli.clean_files")
    def test_multiple_files_partial_failure(self, mock_clean_files):
        """Test processing multiple files with partial failure."""
        # Mock clean_files to return mixed success/failure
        mock_clean_files.return_value = [
            ("file1.py", True, "Success message"),
            ("file2.py", False, "Error message"),
        ]
        
        # Call main with multiple files
        exit_code = main(["file1.py", "file2.py"])
        
        # Check that clean_files was called correctly
        mock_clean_files.assert_called_once()
        
        # Check that the exit code is correct
        assert exit_code == 1

    @patch("pycommentcleaner.cli.clean_files")
    def test_output_dir(self, mock_clean_files):
        """Test processing with output directory."""
        # Mock clean_files to return success
        mock_clean_files.return_value = [
            ("file.py", True, "Success message"),
        ]
        
        # Call main with output directory
        exit_code = main(["file.py", "--output-dir", "output"])
        
        # Check that clean_files was called correctly
        mock_clean_files.assert_called_once()
        args, kwargs = mock_clean_files.call_args
        assert kwargs["output_dir"] == "output"
        
        # Check that the exit code is correct
        assert exit_code == 0