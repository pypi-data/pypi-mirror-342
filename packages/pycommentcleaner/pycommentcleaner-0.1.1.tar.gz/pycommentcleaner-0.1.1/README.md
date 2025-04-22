# PyCommentCleaner

A simple and fast Python utility to remove comments from Python scripts.

## Features

- Removes inline and standalone comments from Python files
- Preserves comments inside strings and docstrings
- Provides both command-line interface and Python API
- Maintains original formatting and whitespace
- Handles complex Python syntax elements correctly

## Installation

```bash
pip install pycommentcleaner
```

## Usage

### Command Line Interface

```bash
# Clean a single file
pycommentcleaner path/to/your_script.py

# Clean multiple files
pycommentcleaner path/to/file1.py path/to/file2.py

# Specify an output directory
pycommentcleaner path/to/file.py --output-dir path/to/output

# Increase verbosity
pycommentcleaner path/to/file.py -v     # Warning level
pycommentcleaner path/to/file.py -vv    # Info level
pycommentcleaner path/to/file.py -vvv   # Debug level

# Show help
pycommentcleaner --help
```

### Python API

```python
# Clean a file
from pycommentcleaner import clean_file

success, message = clean_file("path/to/your_script.py")
print(message)

# Clean code directly
from pycommentcleaner import clean_code

code = """
def hello():
    # This is a comment
    print("Hello, world!")  # This is another comment
    
    # This comment will be removed
    string_with_hash = "This # is not a comment"
"""

cleaned_code = clean_code(code)
print(cleaned_code)
```

## Examples

Before:
```python
# This is a comment at the beginning of the file
def hello():
    # This is a function that prints a greeting
    print("Hello, world!")  # This prints a greeting
    
    string_with_hash = "This # is not a comment"
    """This is a docstring
    # This is not a comment because it's in a docstring
    """
```

After:
```python
 
def hello():
     
    print("Hello, world!")   
    
    string_with_hash = "This # is not a comment"
    """This is a docstring
    # This is not a comment because it's in a docstring
    """
```

## Development

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/viekayy/pycommentcleaner.git
   cd example
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Running Tests

```bash
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- **Viadishwar** - [GitHub](https://github.com/viekayy)