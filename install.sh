#!/usr/bin/env bash

# AI Platform Installation Script
# This script sets up the development environment

set -e

echo "=========================================="
echo "AIDomesticCoreAIJ Setup Script"
echo "=========================================="

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

REQUIRED_VERSION="3.9"
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
    echo "Error: Python 3.9 or higher required"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate || . venv/Scripts/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install development dependencies
echo "Installing development dependencies..."
pip install -r requirements-dev.txt || echo "Note: requirements-dev.txt not found"

# Install pre-commit hooks
echo "Setting up pre-commit hooks..."
pip install pre-commit
pre-commit install || echo "Note: .pre-commit-config.yaml not found"

# Run initial tests
echo ""
echo "Running initial tests..."
pytest tests/ -v --tb=short || echo "Tests completed with some issues"

# Build documentation
echo ""
echo "Building documentation..."
cd docs
sphinx-build -b html . _build/html 2>/dev/null || echo "Note: Documentation build skipped"
cd ..

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To activate the virtual environment:"
echo "  source venv/bin/activate  (on Linux/Mac)"
echo "  venv\\Scripts\\activate    (on Windows)"
echo ""
echo "To run tests:"
echo "  pytest tests/"
echo ""
echo "To build the package:"
echo "  python -m build"
echo ""
echo "To install in development mode:"
echo "  pip install -e ."
echo ""
