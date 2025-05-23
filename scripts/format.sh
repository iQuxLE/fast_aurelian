#!/bin/bash
# Format code using ruff

set -e

echo "🎨 Formatting Fast-Aurelian code..."

# Format with ruff
echo "Running ruff format..."
uv run ruff format src/ tests/

# Sort imports
echo "Sorting imports..."
uv run ruff check --select I --fix src/ tests/

echo "✅ Code formatting completed!"