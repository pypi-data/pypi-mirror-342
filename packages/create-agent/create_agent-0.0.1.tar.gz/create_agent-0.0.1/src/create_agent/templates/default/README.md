# {{ project_title }}

A FastAPI-based service that provides an OpenAI-compatible API interface for LLM-powered agents with RAG (Retrieval Augmented Generation) capabilities.

## Features

- OpenAI-compatible API endpoints for chat completions
- RAG (Retrieval Augmented Generation) implementation using LangGraph
- Streaming response support (SSE)
- Extensible tool system
- Environmental configuration
- Health monitoring

## Getting Started

### Prerequisites

- Python 3.9+
- Virtual environment (recommended)

### Installation

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
cp .env.example .env
```

4. Edit the `.env` file with your configuration:
   - Set `OPENAI_API_KEY` for LLM access
   - Configure `API_KEY` for API authentication
   - Set other optional parameters as needed

### Running the Application

Start the server:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Reference

### `/v1/chat/completions`

Creates a chat completion. Compatible with OpenAI's chat completion API format.

- Method: POST
- Authentication: API key required
- Request body: OpenAI-compatible chat completion request
- Supports streaming with SSE

### `/v1/health`

Health check endpoint.

- Method: GET
- Returns the current status of the service

## Project Structure

- `app/main.py` - FastAPI application setup
- `app/config.py` - Application configuration
- `app/api/` - API definitions and models
- `app/services/` - Business logic services
- `app/rag/` - RAG graph implementation
- `app/core/` - Core functionality
- `app/utils/` - Utility functions

## Extending

### Adding New Tools

To add new tools, edit `app/rag/tools.py` and add your tool definition following the LangChain tool format.

### Customizing RAG

The RAG implementation is in `app/rag/graph.py` and can be customized by modifying the graph structure.
