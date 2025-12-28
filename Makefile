# Makefile for AIDomesticCoreAIJ

.PHONY: help install install-dev test lint format type-check security clean build docs

help:
	@echo "Available commands:"
	@echo "  make install        Install production dependencies"
	@echo "  make install-dev    Install development dependencies"
	@echo "  make test           Run tests"
	@echo "  make test-cov       Run tests with coverage"
	@echo "  make lint           Run linters (flake8, black, isort)"
	@echo "  make format         Format code (black, isort)"
	@echo "  make type-check     Run type checking (mypy)"
	@echo "  make security       Run security checks (bandit, safety)"
	@echo "  make pre-commit     Run pre-commit hooks"
	@echo "  make clean          Clean build artifacts"
	@echo "  make build          Build package"
	@echo "  make docs           Build documentation"
	@echo "  make all            Run all checks"

install:
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt

install-dev:
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=aiplatform --cov=sdk --cov-report=html --cov-report=term-missing

lint:
	flake8 aiplatform sdk tests
	black --check aiplatform sdk tests
	isort --check-only aiplatform sdk tests

format:
	black aiplatform sdk tests examples
	isort aiplatform sdk tests examples

type-check:
	mypy aiplatform sdk --ignore-missing-imports

security:
	bandit -r aiplatform sdk
	safety check

pre-commit:
	pre-commit run --all-files

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .tox -exec rm -rf {} + 2>/dev/null || true
	find . -name .coverage -delete 2>/dev/null || true
	find . -name *.egg-info -type d -exec rm -rf {} + 2>/dev/null || true
	rm -rf build dist .eggs

build: clean
	python -m build

docs:
	cd docs && sphinx-build -b html . _build/html

all: lint type-check security test

.DEFAULT_GOAL := help
