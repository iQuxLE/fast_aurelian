#!/bin/bash
# Run all code quality checks

set -e

echo "🔍 Running comprehensive code quality checks for Fast-Aurelian..."

# Format check
echo ""
echo "1️⃣ Checking code formatting..."
if uv run ruff format --check src/ tests/; then
    echo "✅ Code formatting is correct"
else
    echo "❌ Code formatting issues found. Run 'scripts/format.sh' to fix."
    exit 1
fi

# Linting
echo ""
echo "2️⃣ Running linting checks..."
if uv run ruff check src/ tests/; then
    echo "✅ Linting passed"
else
    echo "❌ Linting issues found"
    exit 1
fi

# Type checking
echo ""
echo "3️⃣ Running type checking..."
if uv run mypy src/; then
    echo "✅ Type checking passed"
else
    echo "❌ Type checking failed"
    exit 1
fi

# Tests
echo ""
echo "4️⃣ Running tests..."
if uv run pytest --tb=short; then
    echo "✅ All tests passed"
else
    echo "❌ Some tests failed"
    exit 1
fi

echo ""
echo "🎉 All checks passed! Your code is ready for commit."