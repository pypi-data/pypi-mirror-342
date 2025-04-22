"""
Command-line interface for the pycommentcleaner package.

This module provides a command-line interface for removing comments
from Python files.
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import List, Optional

from pycommentcleaner.core import clean_file, clean_files


def configure_logging(verbosity: int) -> None:
    """
    Configure logging level based on verbosity.

    Args:
        verbosity: Verbosity level (0-3)
    """
    log_levels = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG
    }
    
    # Set the default level to ERROR if verbosity is out of range
    level = log_levels.get(verbosity, logging.ERROR)
    
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Args:
        args: Command-line arguments (uses sys.argv if None)

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Remove comments from Python files while preserving code functionality."
    )
    
    parser.add_argument(
        "files",
        nargs="+",
        help="Path(s) to Python file(s) to process"
    )
    
    parser.add_argument(
        "-o", "--output-dir",
        help="Directory where cleaned files will be saved (defaults to same directory as input file)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (can be used multiple times, e.g., -vvv)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__import__('pycommentcleaner').__version__}"
    )
    
    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the command-line interface.

    Args:
        args: Command-line arguments (uses sys.argv if None)

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    # Parse command-line arguments
    parsed_args = parse_args(args)
    
    # Configure logging based on verbosity
    configure_logging(parsed_args.verbose)
    
    # Get file paths from arguments
    file_paths = [Path(file_path) for file_path in parsed_args.files]
    
    # Process multiple files
    if len(file_paths) > 1 or parsed_args.output_dir:
        results = clean_files(file_paths, parsed_args.output_dir)
        
        # Print results
        success_count = 0
        for file_path, success, message in results:
            if success:
                success_count += 1
                if parsed_args.verbose > 0:
                    print(message)
            else:
                print(message, file=sys.stderr)
        
        # Print summary
        print(f"Successfully processed {success_count} of {len(file_paths)} files.")
        
        # Return appropriate exit code
        return 0 if success_count == len(file_paths) else 1
    
    # Process a single file
    else:
        file_path = file_paths[0]
        success, message = clean_file(file_path)
        
        if success:
            print(message)
            return 0
        else:
            print(message, file=sys.stderr)
            return 1


if __name__ == "__main__":
    sys.exit(main())