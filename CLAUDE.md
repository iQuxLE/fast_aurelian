# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Fast-Aurelian is a FastAPI-based service that exposes Aurelian agents and tools through a REST API. It allows users to interact with Aurelian's AI agents through HTTP endpoints instead of the command line, enabling integration with other applications and services.

## Development Environment Setup

This project uses uv for dependency management:

```bash
# Install dependencies
uv sync

# Install with development dependencies
uv sync --group dev

# Run development server
uv run uvicorn src.fast_aurelian.main:app --reload --host 0.0.0.0 --port 8000

# Add new dependencies
uv add fastapi uvicorn pydantic

# Add development dependencies
uv add --group dev pytest black flake8 mypy
```

## Project Structure

The project follows a layered architecture:

```
src/fast_aurelian/
├── main.py              # FastAPI application entry point
├── config.py            # Pydantic settings configuration
├── auth.py              # API key authentication
├── api/                 # API route modules
│   ├── routes.py        # Route registration
│   ├── models.py        # Shared Pydantic models
│   ├── paperqa.py       # PaperQA agent endpoints
│   └── diagnosis.py     # Diagnosis agent endpoints
├── services/            # Service layer for agent integration
│   ├── aurelian.py      # Base Aurelian service
│   ├── paperqa.py       # PaperQA service implementation
│   └── diagnosis.py     # Diagnosis service implementation
├── middleware/          # Custom middleware components
│   ├── logging.py       # Request/response logging
│   └── error_handler.py # Consistent error handling
└── utils/               # Utility functions
    ├── async_helpers.py # Async utilities
    └── error_handling.py # Error handling utilities
```

## Common Commands

### Development
```bash
# Start development server with auto-reload
uv run uvicorn src.fast_aurelian.main:app --reload

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src

# Run linting
uv run flake8 src/ tests/
uv run black src/ tests/ --check

# Format code
uv run black src/ tests/

# Type checking
uv run mypy src/
```

### Testing
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_api/test_paperqa.py

# Run tests with verbose output
uv run pytest -v

# Run tests matching pattern
uv run pytest -k "test_paperqa"
```

## Architecture Patterns

### Agent Integration Approaches

**1. Direct Agent Integration** - For simple operations:
```python
from aurelian.agents.paperqa.paperqa_agent import paperqa_agent
from aurelian.agents.paperqa.paperqa_config import get_config

config = get_config()
result = paperqa_agent.run_sync("query", deps=config)
```

**2. CLI Wrapper Integration** - For existing CLI functionality:
```python
from aurelian.agents.paperqa.paperqa_cli import setup_and_configure_paper_directory
from paperqa.agents.search import get_directory_index

paper_dir, settings, _ = setup_and_configure_paper_directory(directory)
index = await get_directory_index(settings=settings, build=True)
```

**3. MCP-based Integration** - For complex workflows:
```python
from mcp.client.remote_tool import MCPTool
from pydantic_ai import Agent

agent = Agent(model="openai:gpt-4o")
agent.tool(MCPTool("paperqa.query_papers"))
result = agent.run_sync("analyze papers about X")
```

### API Endpoint Design

All endpoints follow the pattern: `/api/{agent}/{operation}`

**Standard HTTP methods:**
- GET for retrieval operations
- POST for operations that change state
- PUT for updates
- DELETE for removal operations

**Authentication:** API key in header `X-API-Key: your-api-key`

**Response format:**
```json
{
  "status": "success",
  "data": { ... },
  "metadata": { ... }
}
```

## Environment Configuration

Required environment variables:
```bash
FAST_AURELIAN_API_KEY=your-api-key
FAST_AURELIAN_HOST=0.0.0.0
FAST_AURELIAN_PORT=8000
FAST_AURELIAN_LOG_LEVEL=info
OPENAI_API_KEY=your-openai-key
AURELIAN_WORKDIR=/path/to/workdir
```

## Implementation Guidelines

### Service Layer Pattern
Each Aurelian agent should have a corresponding service class that:
- Handles agent initialization and configuration
- Manages method execution and error handling
- Transforms results for API consumption
- Manages resources and cleanup

### Error Handling
- Use consistent error response format across all endpoints
- Implement proper HTTP status codes
- Log errors with correlation IDs for debugging
- Handle Aurelian-specific exceptions gracefully

### Testing Strategy
- Unit tests for individual components (config, auth, services)
- Integration tests for API endpoints
- End-to-end tests for complete workflows
- Mock external dependencies (Aurelian agents, OpenAI API)

## Dependencies

Core dependencies:
- **FastAPI**: Web framework and API documentation
- **Uvicorn**: ASGI server for production
- **Pydantic**: Data validation and settings management
- **Aurelian**: AI agent framework (external dependency)
- **httpx**: Async HTTP client
- **python-dotenv**: Environment variable loading
- **loguru**: Enhanced logging

Development dependencies:
- **pytest**: Testing framework
- **pytest-asyncio**: Async test support
- **pytest-cov**: Coverage reporting
- **black**: Code formatting
- **flake8**: Linting
- **mypy**: Type checking