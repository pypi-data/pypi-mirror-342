"""Setup script for the Structas package."""
from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="structas",
    version="0.1.0",
    author="",
    author_email="",
    description="A binary for chopping logs...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/author/structas",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "typing-extensions>=4.0.0",
        "pyyaml>=6.0",
        "regex>=2023.0.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "structas=structas.cli:main",
        ],
    },
) 