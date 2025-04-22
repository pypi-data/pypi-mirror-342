# Agentic RAG Boilerplate

A powerful boilerplate for creating Retrieval-Augmented Generation (RAG) applications with agentic capabilities. This template provides a solid foundation for building AI-powered applications that can retrieve and process information intelligently.

## Features

- 🚀 FastAPI-based REST API
- 🤖 LangChain integration for RAG capabilities
- 🔍 Efficient document processing and retrieval
- 🔐 Environment-based configuration
- 📦 Well-structured project layout
- 🛠️ Easy to extend and customize

## Quick Start

### Installation

```bash
pip install create-agentic-rag
```

### Create a New Project

```bash
create-agentic-rag my-project-name
```

This will create a new directory with your project name and set up the basic structure.

### Setup Your Project

1. Navigate to your project directory:

```bash
cd my-project-name
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

4. Configure your environment:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration settings.

### Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Project Structure

```
.
├── app/
│   ├── api/           # API routes and endpoints
│   ├── core/          # Core application logic
│   ├── models/        # Data models
│   ├── services/      # Business logic and services
│   └── main.py        # Application entry point
├── .env.example       # Example environment variables
├── requirements.txt   # Project dependencies
└── README.md         # This file
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

The following environment variables are required:

- `OPENAI_API_KEY`: Your OpenAI API key
- `LANGCHAIN_API_KEY`: Your LangChain API key
- `LANGCHAIN_PROJECT`: Your LangChain project name
- `LANGCHAIN_TRACING_V2`: Enable/disable LangChain tracing
- `LANGCHAIN_ENDPOINT`: LangChain API endpoint

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions, please open an issue in the repository.
