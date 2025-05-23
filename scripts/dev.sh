#!/bin/bash
# Start development server

set -e

echo "🚀 Starting Fast-Aurelian development server..."

# Set development environment variables
export FAST_AURELIAN_DEBUG=true
export FAST_AURELIAN_LOG_LEVEL=debug

# Start the server with auto-reload
echo "Server will be available at: http://localhost:8000"
echo "API documentation at: http://localhost:8000/docs"
echo "Press Ctrl+C to stop the server"
echo ""

uv run uvicorn src.fast_aurelian.main:app \
    --reload \
    --host 0.0.0.0 \
    --port 8000 \
    --log-level debug