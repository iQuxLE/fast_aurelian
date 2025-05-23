# Fast-Aurelian

A FastAPI-based microservice that exposes Aurelian PaperQA agents and tools through a REST API, enabling scientific paper search, indexing, and Q&A capabilities.

## Overview

Fast-Aurelian provides a thin REST API layer over Aurelian's PaperQA functionality, allowing you to:

- **Add papers** from URLs or local files to a searchable collection
- **Index paper collections** for fast semantic search  
- **Query papers** with natural language questions and get AI-powered answers
- **Search for new papers** from scientific databases
- **List and manage** your paper collections

## Features

- 🚀 **FastAPI**: Modern, fast web framework with automatic API documentation
- 🔍 **PaperQA Integration**: Direct integration with Aurelian's PaperQA tools
- 📄 **Multi-format Support**: PDF, TXT, HTML, and Markdown files
- 🤖 **AI-Powered Q&A**: GPT-4 powered question answering over your papers
- ⚡ **Async Processing**: Efficient handling of concurrent requests
- 📊 **Type Safety**: Full Pydantic validation for requests and responses
- 🗂️ **Index Management**: Persistent paper indexing with vector search

## Prerequisites

- Python 3.11+ (3.13 not supported due to dependency issues)
- OpenAI API key
- [uv](https://github.com/astral-sh/uv) package manager

## Installation

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/fast-aurelian.git
cd fast-aurelian
```

### 2. Install Dependencies

```bash
# Install all dependencies including Aurelian
uv sync

# Or if you have Aurelian installed separately
uv install
```

### 3. Environment Variables

Create a `.env` file or set environment variables:

```bash
# Required
export OPENAI_API_KEY="your-openai-api-key"

# Optional
export FAST_AURELIAN_LOG_LEVEL="INFO"
export FAST_AURELIAN_DEBUG="true"
```

## Quick Start

### 1. Start the Server

```bash
# Using uv
uv run uvicorn src.fast_aurelian.main:app --reload --port 8002

# Or using the development script
chmod +x scripts/dev.sh
./scripts/dev.sh
```

### 2. Access API Documentation

- **Swagger UI**: http://localhost:8002/docs
- **ReDoc**: http://localhost:8002/redoc
- **Health Check**: http://localhost:8002/health

### 3. Example Workflow

```bash
# 1. Add a paper
curl -X POST "http://localhost:8002/api/paperqa/add" \
  -H "Content-Type: application/json" \
  -d '{"path": "https://arxiv.org/pdf/1706.03762.pdf", "citation": "Attention Is All You Need"}'

# 2. Index papers (make them searchable)
curl -X POST "http://localhost:8002/api/paperqa/index" \
  -H "Content-Type: application/json" \
  -d '{"directory": "./papers"}'

# 3. Query your papers
curl -X POST "http://localhost:8002/api/paperqa/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the attention mechanism?"}'

# 4. List all papers
curl -X GET "http://localhost:8002/api/paperqa/list"
```

## API Endpoints

### Core PaperQA Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/paperqa/query` | Answer questions using indexed papers |
| `POST` | `/api/paperqa/search` | Search for papers online |
| `POST` | `/api/paperqa/add` | Add a paper from URL or file path |
| `POST` | `/api/paperqa/index` | Index papers in a directory |
| `GET`  | `/api/paperqa/list` | List papers in collection |

### Request/Response Examples

**Add Paper**:
```json
POST /api/paperqa/add
{
  "path": "https://arxiv.org/pdf/1706.03762.pdf",
  "citation": "Vaswani et al. (2017). Attention Is All You Need."
}
```

**Query Papers**:
```json
POST /api/paperqa/query
{
  "query": "How does the transformer architecture work?"
}
```

**Index Directory**:
```json
POST /api/paperqa/index
{
  "directory": "/path/to/papers"
}
```

## Development

### Project Structure

```
fast-aurelian/
├── src/fast_aurelian/          # Main application code
│   ├── api/                    # API routes and endpoints
│   ├── services/               # Business logic and Aurelian integration
│   ├── middleware/             # HTTP middleware
│   └── config.py               # Configuration management
├── tests/                      # Test suite
├── scripts/                    # Development scripts
└── pyproject.toml              # Project configuration
```

### Development Commands

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src

# Format code
./scripts/format.sh

# Lint code  
./scripts/lint.sh

# Type checking
uv run mypy src

# Run all checks
./scripts/check.sh
```

### Testing

The project includes comprehensive test coverage:

- **Unit tests**: Mock-based testing of individual components
- **Integration tests**: End-to-end testing with real Aurelian functions
- **API tests**: FastAPI route and validation testing

```bash
# Run specific test categories
uv run pytest tests/test_api.py          # API tests
uv run pytest tests/integration.py      # Integration tests
uv run pytest tests/test_services.py    # Service tests
```

## Current Status

### ✅ Working Features
- FastAPI application with proper routing
- Aurelian PaperQA integration
- Paper indexing and search capabilities
- Comprehensive test suite
- Development tooling (linting, formatting, type checking)

### ⚠️ Known Limitations
- Index directory consistency needs improvement (see [INDEXING_STRATEGY.md](INDEXING_STRATEGY.md))
- Python 3.13 compatibility issues with some dependencies
- Limited error handling for edge cases

### 🚧 Planned Improvements
- Unified paper index management
- Better file organization and naming
- Web interface for paper management
- Advanced search and filtering options

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | - |
| `FAST_AURELIAN_LOG_LEVEL` | Logging level | `INFO` |
| `FAST_AURELIAN_DEBUG` | Debug mode | `false` |
| `FAST_AURELIAN_HOST` | Server host | `127.0.0.1` |
| `FAST_AURELIAN_PORT` | Server port | `8000` |

### Papers Directory

By default, papers are stored in a `papers/` directory relative to where you start the server. The index (`.pqa` folder) is created in the same location.

## Troubleshooting

### Common Issues

1. **"No papers indexed" error**: Run the index endpoint before querying
2. **Authentication errors**: Ensure `OPENAI_API_KEY` is set correctly  
3. **Import errors**: Use Python 3.11 or 3.12 (not 3.13)
4. **Port conflicts**: Use `--port 8002` or another available port

### Debug Mode

Enable debug logging for troubleshooting:

```bash
export FAST_AURELIAN_LOG_LEVEL="DEBUG"
uv run uvicorn src.fast_aurelian.main:app --reload --port 8002
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run the test suite: `./scripts/check.sh`
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details

## Related Projects

- [Aurelian](https://github.com/monarch-initiative/aurelian) - The underlying AI agent framework
- [PaperQA](https://github.com/whitead/paper-qa) - Scientific paper Q&A library
- [Monarch Initiative](https://monarchinitiative.org/) - Biomedical data integration platform