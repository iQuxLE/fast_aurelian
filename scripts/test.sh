#!/bin/bash
# Run tests with coverage reporting

set -e

echo "🧪 Running Fast-Aurelian tests..."

# Run tests with coverage
poetry run pytest

# Generate coverage report
echo ""
echo "📊 Coverage Summary:"
poetry run coverage report

# Optional: Open HTML coverage report
if [[ "$1" == "--open" ]]; then
    echo "📈 Opening HTML coverage report..."
    if command -v open >/dev/null 2>&1; then
        open htmlcov/index.html
    elif command -v xdg-open >/dev/null 2>&1; then
        xdg-open htmlcov/index.html
    else
        echo "HTML coverage report available at: htmlcov/index.html"
    fi
fi

echo "✅ All tests completed!"