"""
Setup configuration for the pycommentcleaner package.
"""

import os
from setuptools import setup, find_packages

# Read the contents of the README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Get version from package __init__.py
with open(os.path.join("pycommentcleaner", "__init__.py"), encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break

setup(
    name="pycommentcleaner",
    version=version,
    author="Viadishwar",
    author_email="viekayy.1234@gmail.com",
    description="A simple and fast Python utility to remove comments from Python scripts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/viekayy/pycommentcleaner.git",
    packages=find_packages(exclude=["tests", "examples"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "pycommentcleaner=pycommentcleaner.cli:main",
        ],
    },
    keywords="python, comments, cleaner, utility, development",
)