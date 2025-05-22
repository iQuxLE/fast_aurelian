# Fast-Aurelian

A FastAPI-based service that exposes Aurelian agents and tools through a REST API.

## Overview

Fast-Aurelian provides a RESTful API interface to Aurelian's AI agents, allowing you to use them from any application or service that can make HTTP requests.

## Features

- **PaperQA API**: Query scientific papers, search for papers, add papers to the collection, and index paper directories
- **FastAPI Integration**: Leverages FastAPI for fast, type-safe API development with automatic documentation
- **Async Processing**: Uses async/await for efficient handling of concurrent requests
- **Error Handling**: Consistent error responses with detailed information
- **Logging**: Structured logging with correlation IDs

## Installation

### Prerequisites

- Python 3.11+
- [Aurelian](https://github.com/monarch-initiative/aurelian) installation

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/fast-aurelian.git
   cd fast-aurelian
   ```

2. Install Aurelian:
   ```bash
   pip install git+https://github.com/monarch-initiative/aurelian.git
   ```

3. Install Fast-Aurelian:
   ```bash
   pip install -e .
   ```

## Usage

### Starting the API Server

```bash
uvicorn fast_aurelian.main:app --reload
```

The API will be available at http://127.0.0.1:8000.

### API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Environment Variables

Configure the application using these environment variables:

- `FAST_AURELIAN_HOST`: Host to bind to (default: 127.0.0.1)
- `FAST_AURELIAN_PORT`: Port to listen on (default: 8000)
- `FAST_AURELIAN_LOG_LEVEL`: Logging level (default: INFO)
- `OPENAI_API_KEY`: Your OpenAI API key (required for PaperQA)
- `PAPERQA_WORK_DIR`: Directory for PaperQA operations (default: /tmp/paperqa_work)

## API Endpoints

### PaperQA

- `POST /api/paperqa/query`: Query papers to answer a specific question
- `POST /api/paperqa/search`: Search for papers relevant to a query
- `POST /api/paperqa/add`: Add a paper to the collection
- `POST /api/paperqa/index`: Index papers in a directory
- `GET /api/paperqa/list`: List all papers in the collection

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black src tests
flake8 src tests
mypy src
```

## License

[MIT License](LICENSE)