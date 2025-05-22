# Fast-Aurelian Architecture

## Overview

Fast-Aurelian is a FastAPI-based service that exposes Aurelian agents and tools through a REST API. It allows users to interact with Aurelian's AI agents through HTTP endpoints instead of the command line, enabling integration with other applications and services.

## Core Principles

1. **Standalone Service**: Fast-Aurelian is a separate application that depends on Aurelian but doesn't modify it.
2. **Clean API Design**: Well-documented endpoints with consistent patterns and error handling.
3. **Asynchronous**: Leverages FastAPI's async capabilities for handling concurrent requests.
4. **Authentication**: Simple API key authentication for securing endpoints.
5. **Configurable**: Easy configuration for agent settings and deployment options.
6. **Single Responsibility**: Each component has a clear, focused responsibility.

## Folder Structure

```
fast-aurelian/
├── .github/                      # GitHub workflows for CI/CD
│   └── workflows/
│       ├── lint.yml
│       ├── test.yml
│       └── build.yml
├── .gitignore                    # Git ignore file
├── README.md                     # Project documentation
├── pyproject.toml                # Poetry project configuration
├── poetry.lock                   # Poetry lock file
├── docs/                         # Documentation
│   └── api/                      # API documentation
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py               # Test fixtures
│   ├── test_api/                 # API tests
│   │   ├── __init__.py
│   │   ├── test_paperqa.py       # PaperQA API tests
│   │   └── ...
│   └── test_services/            # Service tests
├── src/
│   └── fast_aurelian/
│       ├── __init__.py
│       ├── config.py             # Configuration management
│       ├── main.py               # FastAPI application entry point
│       ├── auth.py               # Authentication modules
│       ├── middleware/           # Middleware components
│       │   ├── __init__.py
│       │   ├── logging.py        # Logging middleware
│       │   └── error_handler.py  # Error handling middleware
│       ├── api/                  # API routes
│       │   ├── __init__.py
│       │   ├── routes.py         # Route registration
│       │   ├── models.py         # Shared Pydantic models
│       │   ├── paperqa.py        # PaperQA routes
│       │   ├── diagnosis.py      # Diagnosis routes
│       │   └── ...               # Other agent routes
│       ├── services/             # Service layer
│       │   ├── __init__.py
│       │   ├── aurelian.py       # Base Aurelian service
│       │   ├── paperqa.py        # PaperQA service
│       │   └── ...               # Other agent services
│       └── utils/                # Utility functions
│           ├── __init__.py
│           ├── async_helpers.py  # Async utilities
│           └── error_handling.py # Error handling utilities
└── scripts/                      # Utility scripts
    ├── start_dev.sh              # Development startup script
    └── test_api.sh               # API test script
```

## Component Descriptions

### 1. FastAPI Application (`main.py`)

The main FastAPI application that configures middleware, routes, and serves the API. It loads configuration from environment variables or a config file and initializes the necessary services.

**Responsibilities:**
- Application initialization
- Middleware configuration
- Route registration
- CORS settings
- Documentation setup (Swagger/ReDoc)

### 2. Configuration (`config.py`)

Manages application configuration using Pydantic settings, loading from environment variables and config files.

**Responsibilities:**
- Configuration loading and validation
- Environment variable parsing
- Default configuration values
- Configuration type conversion

**Key Configuration Areas:**
- API settings (host, port, debug mode)
- Authentication settings
- Aurelian agent settings
- Logging configuration

### 3. Authentication (`auth.py`)

Implements API key authentication for securing endpoints.

**Responsibilities:**
- API key validation
- Dependency injection for protected routes
- Authentication error handling

### 4. API Routes

Each Aurelian agent has its own route module in the `api/` directory.

**Responsibilities (per route module):**
- Define endpoints for a specific agent
- Input validation using Pydantic models
- Route handling logic
- Response formatting
- Error classification

**Example Modules:**
- `paperqa.py`: Routes for PaperQA agent
- `diagnosis.py`: Routes for Diagnosis agent

### 5. Service Layer

The service layer acts as an intermediary between the API routes and Aurelian.

**Responsibilities (per service):**
- Agent initialization and configuration
- Method execution and error handling
- Result transformation
- Resource management

**Example Services:**
- `paperqa.py`: PaperQA agent service
- `diagnosis.py`: Diagnosis agent service

### 6. Middleware

Custom middleware components for cross-cutting concerns.

**Responsibilities:**
- Request/response logging with correlation IDs
- Consistent error handling
- Performance monitoring
- Request validation

## Communication Flow

```
Client → FastAPI App → API Routes → Services → Aurelian Agents → Results → Client
```

1. **Client sends request**: HTTP request to an endpoint
2. **FastAPI validates**: Request validation and authentication
3. **Route handler**: Processes the request and calls the appropriate service
4. **Service layer**: Initializes the Aurelian agent and calls its methods
5. **Aurelian agent**: Performs the requested operation
6. **Results transformation**: Service transforms the results to API response format
7. **Response**: Formatted response sent back to the client

## Agent Integration Patterns

Fast-Aurelian provides three ways to integrate with Aurelian agents:

### 1. Direct Agent Integration

For simple operations, directly imports and uses Aurelian agent classes.

**When to use:**
- Simple, straightforward agent operations
- When you need direct control over agent initialization
- For low-latency requirements

**Example:**
```python
from aurelian.agents.paperqa.paperqa_agent import paperqa_agent
from aurelian.agents.paperqa.paperqa_config import get_config

# Initialize agent
config = get_config()
result = paperqa_agent.run_sync("query papers about X", deps=config)
```

### 2. CLI Wrapper Integration

For operations that are already well-implemented in the Aurelian CLI.

**When to use:**
- Complex operations already implemented in CLI
- When you need to maintain CLI compatibility
- For file/directory operations

**Example:**
```python
import asyncio
from aurelian.agents.paperqa.paperqa_cli import setup_and_configure_paper_directory, get_document_files
from paperqa.agents.search import get_directory_index

# Use CLI functions
paper_dir, settings, _ = setup_and_configure_paper_directory(directory)
index = await get_directory_index(settings=settings, build=True)
```

### 3. MCP-based Integration

For complex operations that benefit from MCP's tool architecture.

**When to use:**
- When combining multiple agent capabilities
- For complex workflows that span multiple tools
- When you need tool composition

**Example:**
```python
from mcp.client.remote_tool import MCPTool
from pydantic_ai import Agent

# Start MCP server in background
# ...

# Create agent with MCP tools
agent = Agent(model="openai:gpt-4o")
agent.tool(MCPTool("paperqa.query_papers"))
result = agent.run_sync("analyze papers about X")
```

## API Endpoint Design

Endpoints follow a consistent design pattern:

**Path structure:**
```
/api/{agent}/{operation}
```

**Example endpoints:**
- `POST /api/paperqa/query` - Query papers
- `POST /api/paperqa/add` - Add a paper
- `POST /api/paperqa/index` - Index papers
- `GET /api/paperqa/list` - List papers

**Common patterns:**
- GET for retrieval operations
- POST for operations that change state
- PUT for updates
- DELETE for removal operations

**Authentication:**
- API key in header: `X-API-Key: your-api-key`

**Response format:**
```json
{
  "status": "success",
  "data": { ... },
  "metadata": { ... }
}
```

**Error format:**
```json
{
  "status": "error",
  "error": {
    "code": "error_code",
    "message": "Error message",
    "details": { ... }
  }
}
```

## Deployment Options

Fast-Aurelian can be deployed in several ways:

1. **Standalone Service**: Run as an independent service that connects to Aurelian
2. **Docker Container**: Packaged with Aurelian dependencies
3. **Kubernetes**: Deploy as part of a larger application stack
4. **Serverless**: Deploy as a serverless function (with some limitations)

## Environment Configuration

Key environment variables:

```
FAST_AURELIAN_API_KEY=your-api-key
FAST_AURELIAN_HOST=0.0.0.0
FAST_AURELIAN_PORT=8000
FAST_AURELIAN_LOG_LEVEL=info
OPENAI_API_KEY=your-openai-key
AURELIAN_WORKDIR=/path/to/workdir
```

## Dependencies

- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **Aurelian**: AI agent framework
- **httpx**: Async HTTP client
- **python-dotenv**: Environment variable loading
- **loguru**: Improved logging