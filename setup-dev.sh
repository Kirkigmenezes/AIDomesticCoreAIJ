#!/bin/bash
# Setup script for development environment

echo "=========================================="
echo "AI Platform SDK - Development Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
MIN_VERSION="3.9"

if [[ "$PYTHON_VERSION" < "$MIN_VERSION" ]]; then
    echo "❌ Python $MIN_VERSION or higher required (found $PYTHON_VERSION)"
    exit 1
fi
echo "✅ Python $PYTHON_VERSION found"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel
echo "✅ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Install dev dependencies
echo "Installing development dependencies..."
pip install -r requirements-dev.txt
echo "✅ Development dependencies installed"
echo ""

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install
echo "✅ Pre-commit hooks installed"
echo ""

# Run tests
echo "Running tests..."
pytest tests/ -v --tb=short
echo ""

# Display status
echo "=========================================="
echo "✅ Development environment setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Activate environment: source venv/bin/activate"
echo "  2. Run tests:            pytest tests/"
echo "  3. Format code:          black aiplatform tests"
echo "  4. Check quality:        flake8 aiplatform tests"
echo ""
