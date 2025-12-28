#!/bin/sh
# Install pre-commit framework
pip install pre-commit

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
