# create-agent

A CLI tool to quickly scaffold LLM agent API projects with an OpenAI-compatible interface.

## Features

- Create a new agent project with a single command
- Includes ready-to-use API endpoints compatible with OpenAI's chat completion API
- Built-in RAG (Retrieval Augmented Generation) capabilities using LangGraph
- Support for custom tool definitions
- Complete FastAPI application structure

## Installation

```bash
pip install create-agent
```

## Usage

Create a new agent project:

```bash
create-agent my-agent
```

This will create a new directory called `my-agent` with all the necessary files to run an agent API.

### Options

- `--template`: Specify a template to use (default: "default")
- `--output-dir`: Specify the output directory (default: current directory)

```bash
create-agent my-agent --output-dir projects
```

## Project Structure

The generated project follows a well-organized structure:

```
my-agent/
├── app/
│   ├── api/            # API definitions and models
│   ├── core/           # Core functionality
│   ├── rag/            # RAG implementation with LangGraph
│   ├── services/       # Business logic services
│   ├── utils/          # Utility functions
│   ├── config.py       # Application configuration
│   └── main.py         # FastAPI application
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore file
├── README.md           # Project documentation
└── requirements.txt    # Dependencies
```

## Next Steps After Creating a Project

1. Navigate to your new project directory:

   ```bash
   cd my-agent
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:

   ```bash
   cp .env.example .env
   ```

5. Edit the `.env` file with your API keys and configuration

6. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## License

MIT
