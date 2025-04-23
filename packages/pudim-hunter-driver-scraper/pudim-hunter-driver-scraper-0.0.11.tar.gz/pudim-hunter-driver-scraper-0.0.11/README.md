# Pudim Hunter Driver Scraper 🍮

[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Pytest 7.4](https://img.shields.io/badge/pytest-7.4-brightgreen.svg)](https://docs.pytest.org/en/7.4.x/)
[![CI](https://github.com/luismr/pudim-hunter-driver-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/luismr/pudim-hunter-driver-scraper/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/luismr/pudim-hunter-driver-scraper/branch/main/graph/badge.svg)](https://codecov.io/gh/luismr/pudim-hunter-driver-scraper)
[![PyPI version](https://badge.fury.io/py/pudim-hunter-driver-scraper.svg)](https://pypi.org/project/pudim-hunter-driver-scraper/)

## Table of Contents

* Features
* Usage
  * Installation
  * Interface Overview
* Project Structure
* Installation
* Virtual Environment Setup
  * Prerequisites
  * macOS and Linux
  * Windows
  * Troubleshooting
* Development
* Contributing
  * Getting Started
  * Pull Request Process
  * Repository
* License

A Python package that provides a Playwright-based scraper implementation for The Pudim Hunter platform. This package extends the `pudim-hunter-driver` interface to provide a common base for implementing job board scrapers.

## Features

* Playwright-based web scraping
* Async support for better performance
* Headless browser automation
* Easy-to-extend base classes for job board implementations
* Built-in error handling and resource management
* Type hints and validation using Pydantic

## Usage

### Installation

You can install the package directly from PyPI:

```bash
# Install directly using pip
pip install pudim-hunter-driver-scraper

# Or add to your requirements.txt
pudim-hunter-driver-scraper>=0.0.1  # Replace with the version you need
```

For development installations, see the Development section.

### Interface Overview

This package provides the base scraper implementation for job search drivers. To create a scraper for a specific job board, you'll need to extend the `ScraperJobDriver` class and implement the required methods.

1. `ScraperJobDriver` (ABC) - The base scraper class that implements `JobDriver`:
   * `async build_search_url(query: JobQuery) -> str`
   * `def get_selectors() -> Dict[str, str]`
   * `def transform_data(data: Dict[str, Any]) -> Optional[Job]`

2. `PlaywrightScraper` - The base scraper implementation:
   * Supports both sync and async operations
   * Handles browser lifecycle
   * Provides navigation and data extraction methods

3. Exceptions:
   * Inherits all exceptions from `pudim-hunter-driver`
   * Adds scraper-specific error handling

## Project Structure

```
pudim-hunter-driver-scraper/
├── src/
│   └── pudim_hunter_driver_scraper/
│       ├── __init__.py          # Package initialization
│       ├── scraper.py           # PlaywrightScraper implementation
│       └── driver.py            # ScraperJobDriver implementation
├── tests/                       # Test directory
│   └── __init__.py
├── README.md                    # This file
├── requirements.txt             # Direct dependencies
├── setup.py                     # Package setup
└── pyproject.toml              # Project configuration
```

## Installation

From PyPI:
```bash
pip install pudim-hunter-driver-scraper
```

From source:
```bash
git clone git@github.com:luismr/pudim-hunter-driver-scraper.git
cd pudim-hunter-driver-scraper
pip install -r requirements.txt
```

For development:
```bash
pip install -e .
```

## Virtual Environment Setup

We strongly recommend using a virtual environment for development and testing. This isolates the project dependencies from your system Python packages.

### Prerequisites

* Python 3.9 or higher
* pip (Python package installer)
* venv module (usually comes with Python 3)

### macOS and Linux

1. Open Terminal and navigate to the project directory:
```bash
cd pudim-hunter-driver-scraper
```

2. Create a virtual environment:
```bash
python3.9 -m venv venv
```

3. Activate the virtual environment:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e .  # for development
```

5. Install Playwright browsers:
```bash
playwright install chromium
```

6. To deactivate when done:
```bash
deactivate
```

### Windows

1. Open Command Prompt or PowerShell and navigate to the project directory:
```bash
cd pudim-hunter-driver-scraper
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
* In Command Prompt:
```bash
.\venv\Scripts\activate.bat
```
* In PowerShell:
```bash
.\venv\Scripts\Activate.ps1
```

4. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e .  # for development
```

5. Install Playwright browsers:
```bash
playwright install chromium
```

6. To deactivate when done:
```bash
deactivate
```

### Troubleshooting

#### macOS/Linux

* If `python3.9` is not found, install it using your package manager:
  * macOS (with Homebrew): `brew install python@3.9`
  * Ubuntu/Debian: `sudo apt-get install python39 python39-venv`
  * CentOS/RHEL: `sudo yum install python39 python39-devel`

#### Windows

* Ensure Python is added to your PATH during installation
* If PowerShell execution policy prevents activation:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Development

1. Create and activate a virtual environment:
```bash
python3.9 -m venv venv
source venv/bin/activate
```

2. Install in development mode:
```bash
pip install -e .
```

## Contributing

We love your input! We want to make contributing to Pudim Hunter Driver Scraper as easy and transparent as possible, whether it's:

* Reporting a bug
* Discussing the current state of the code
* Submitting a fix
* Proposing new features
* Becoming a maintainer

### Getting Started

1. Fork the repository
```bash
# Clone the repository
git clone git@github.com:luismr/pudim-hunter-driver-scraper.git
cd pudim-hunter-driver-scraper
# Create your feature branch
git checkout -b feature/amazing-feature
# Set up development environment
python3.9 -m venv venv
source venv/bin/activate
pip install -e .
```

2. Make your changes
   * Write clear, concise commit messages
   * Add tests for any new functionality
   * Ensure all tests pass: `pytest tests/ -v`

3. Push to your fork and submit a pull request
```bash
git push origin feature/amazing-feature
```

### Pull Request Process

1. Update the README.md with details of changes if needed
2. Add any new dependencies to requirements.txt
3. Update the tests if needed
4. The PR will be merged once you have the sign-off of the maintainers

### Repository

* Main repository: github.com/luismr/pudim-hunter-driver-scraper
* Issue tracker: github.com/luismr/pudim-hunter-driver-scraper/issues

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

Copyright (c) 2024-2025 Luis Machado Reis 