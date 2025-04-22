"""
Core functionality for removing comments from Python code.

This module contains the main logic for parsing Python code and
removing comments while preserving code inside strings and docstrings.
"""

import logging
import os
import tokenize
from io import StringIO
from pathlib import Path
from typing import List, Optional, Tuple, Union

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def clean_code(code: str) -> str:
    """
    Remove comments from Python code while preserving indentation.

    Args:
        code: Python code as a string

    Returns:
        Python code with comments removed
    """
    logger.debug("Cleaning code snippet")
    result = []
    source = StringIO(code)

    try:
        tokens = tokenize.generate_tokens(source.readline)

        for tok in tokens:
            tok_type = tok.type
            tok_string = tok.string

            # Skip comment tokens
            if tok_type == tokenize.COMMENT:
                logger.debug(f"Removed comment: {tok_string}")
                continue
            result.append(tok)

        # Reconstruct the code with original formatting
        return tokenize.untokenize(result)
    
    except tokenize.TokenError as e:
        logger.error(f"Tokenization error: {e}")
        return code
    except Exception as e:
        logger.error(f"Unexpected error during code cleaning: {e}")
        return code


def clean_file(file_path: Union[str, Path], output_path: Optional[Union[str, Path]] = None) -> Tuple[bool, str]:
    """
    Remove comments from a Python file and save the result.

    Args:
        file_path: Path to the Python file
        output_path: Path where the cleaned file will be saved. If None,
                     a file with '_cleaned' suffix will be created in the same directory.

    Returns:
        Tuple of (success: bool, message: str)
    """
    file_path = Path(file_path)

    try:
        if not file_path.exists():
            error_msg = f"File not found: {file_path}"
            logger.error(error_msg)
            return False, error_msg

        if file_path.suffix.lower() != '.py':
            error_msg = f"Not a Python file: {file_path}"
            logger.error(error_msg)
            return False, error_msg

        if output_path is None:
            file_stem = file_path.stem
            output_path = file_path.parent / f"{file_stem}_cleaned.py"
        else:
            output_path = Path(output_path)

        logger.info(f"Cleaning file: {file_path}")
        logger.info(f"Output file: {output_path}")

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        cleaned_content = clean_code(content)

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_content)

        success_msg = f"Successfully cleaned {file_path} -> {output_path}"
        logger.info(success_msg)
        return True, success_msg

    except Exception as e:
        error_msg = f"Error cleaning file {file_path}: {str(e)}"
        logger.error(error_msg)
        return False, error_msg


def clean_files(file_paths: List[Union[str, Path]], output_dir: Optional[Union[str, Path]] = None) -> List[Tuple[str, bool, str]]:
    """
    Remove comments from multiple Python files.

    Args:
        file_paths: List of paths to Python files
        output_dir: Directory where cleaned files will be saved. If None,
                    files with '_cleaned' suffix will be created in the same directory.

    Returns:
        List of tuples with (file_path, success, message) for each processed file
    """
    results = []

    for file_path in file_paths:
        file_path = Path(file_path)

        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{file_path.stem}_cleaned.py"
        else:
            output_path = None

        success, message = clean_file(file_path, output_path)
        results.append((str(file_path), success, message))

    return results
