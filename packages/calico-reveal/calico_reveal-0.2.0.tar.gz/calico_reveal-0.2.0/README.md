# calico-reveal

[![PyPI](https://img.shields.io/pypi/v/calico-reveal.svg)](https://pypi.org/project/calico-reveal/)
[![Changelog](https://img.shields.io/github/v/release/nanuxbe/calico-reveal?include_prereleases&label=changelog)](https://github.com/nanuxbe/calico-reveal/releases)
[![Tests](https://github.com/nanuxbe/calico-reveal/workflows/Test/badge.svg)](https://github.com/nanuxbe/calico-reveal/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/nanuxbe/calico-reveal/blob/main/LICENSE)

A Calico plugin to build widget documentation

## Installation

First configure your Django project [to use DJP](https://djp.readthedocs.io/en/latest/installing_plugins.html).

Then install this plugin in the same environment as your Django application.
```bash
pip install calico-reveal
```
## Usage

Usage instructions go here.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd calico-reveal
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
