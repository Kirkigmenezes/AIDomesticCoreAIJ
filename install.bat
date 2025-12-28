@echo off
REM AI Platform Installation Script for Windows

echo ==========================================
echo AIDomesticCoreAIJ Setup Script - Windows
echo ==========================================

REM Check Python version
python --version
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Install development dependencies
echo Installing development dependencies...
pip install -r requirements-dev.txt 2>nul || echo Note: requirements-dev.txt not found

REM Install pre-commit hooks
echo Setting up pre-commit hooks...
pip install pre-commit
pre-commit install 2>nul || echo Note: .pre-commit-config.yaml not found

REM Run initial tests
echo.
echo Running initial tests...
pytest tests/ -v --tb=short 2>nul || echo Tests completed with some issues

REM Build documentation
echo.
echo Building documentation...
cd docs
sphinx-build -b html . _build\html 2>nul || echo Note: Documentation build skipped
cd ..

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo To activate the virtual environment:
echo   venv\Scripts\activate
echo.
echo To run tests:
echo   pytest tests\
echo.
echo To build the package:
echo   python -m build
echo.
echo To install in development mode:
echo   pip install -e .
echo.
