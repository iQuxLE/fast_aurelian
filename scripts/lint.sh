#!/bin/bash
# Run linting and type checking

set -e

echo "🔍 Linting Fast-Aurelian code..."

# Run ruff linting
echo "Running ruff check..."
uv run ruff check src/ tests/

# Run type checking
echo "Running mypy type checking..."
uv run mypy src/

echo "✅ Linting completed successfully!"