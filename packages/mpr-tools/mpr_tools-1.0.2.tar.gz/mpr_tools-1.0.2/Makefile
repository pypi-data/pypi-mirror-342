# ==========================
# CONFIGURATION
# ==========================
# Makefile for Python Development Environment

# Specify the shell to use
SHELL := /bin/bash

# Variables
VENV_DIR = .venv
PYTHON_VERSION = python3.10
BIN = $(VENV_DIR)/bin

LINT_DIRECTORIES = ./{src,tests}

# Default goal
.DEFAULT_GOAL :=help


# ==========================
# SETUP STAGE
# ==========================

# Default target: setup everything
all: venv install

# Create a virtual environment 
venv:
	@echo "🔹 Creating virtual environment in $(VENV_DIR)..."
	$(PYTHON_VERSION) -m venv $(VENV_DIR)
	$(BIN)/pip install --upgrade pip
	@echo "✅ Virtual environment created."

# Install dependencies
install: venv
	@echo "🔹 Installing dependencies..."
	$(BIN)/pip install -e .
	@echo "✅ Dependencies installed."

install_dev: venv install
	@echo "🔹 Installing dev dependencies..."
	$(BIN)/pip install -e '.[dev]'
	@echo "✅ Dev dependencies installed."


# ==========================
# BUILD STAGE
# ==========================

# Build a Python package (assuming a pyproject.toml-based project)
build: install
	@echo "🔹 Building the package..."
	$(bin)/python -m build
	@echo "✅ Build completed."


# ==========================
# DEVELOPMENT STAGE
# ==========================

# Run tests with pytest
test: install_dev
	@echo "🔹 Running tests..."
	$(BIN)/pytest
	@echo "✅ Tests completed."

# Format code with Black
format: install_dev
	@echo "🔹 Formatting code..."
	$(BIN)/black $(LINT_DIRECTORIES)
	@echo "✅ Code formatted."

# Lint with Flake8 & Pylint
lint: install_dev
	@echo "🔹 Linting the code with flake8..."
	$(BIN)/flake8 $(LINT_DIRECTORIES)
	@echo "✅ Linting with flake8 completed."
	@echo "🔹 Linting the code with pylint..."
	$(BIN)/pylint $(LINT_DIRECTORIES)
	@echo "✅ Linting with pylint completed."


# ==========================
# CLEANUP STAGE
# ==========================

# Remove virtual environment
clean:
	@echo "🔹 Removing virtual environment..."
	rm -rf $(VENV_DIR)
	@echo "✅ Virtual environment removed."

# Remove cache & compiled files
clean-pyc:
	@echo "🔹 Cleaning Python cache files..."
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	@echo "✅ Python cache files removed."


.PHONY: all venv install install_dev build test format lint clean clean-pyc
