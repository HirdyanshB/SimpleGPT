# SimpleGPT

SimpleGPT is an open-source **agentic AI chatbot** built with **Python, FastAPI, LangGraph, LangChain, Google Gemini, Tavily, ChromaDB, and SQLite**.

It supports real-time streaming chat, document uploads, retrieval-augmented generation (RAG), web search, conversation memory, and a simple web UI.

---

## Features

* Chat with an AI agent powered by Google Gemini
* Stream responses in real time
* Upload documents such as PDF, DOCX, TXT, MD, PY, and CSV
* Use uploaded files as context through RAG
* Search the web with Tavily for current information
* Store and recall conversation history
* Simple FastAPI-based web interface
* Docker-ready deployment

---

## Project Overview

This project combines:

* **FastAPI** for the backend server and API endpoints
* **Jinja2** for rendering the frontend UI
* **LangGraph** for agent orchestration
* **LangChain** for tools, messages, and RAG workflow
* **Google Gemini** as the LLM provider
* **Tavily** for web search
* **ChromaDB** for vector search over uploaded documents
* **SQLite** for conversation and persistence
* **Docker** for containerized deployment

---

## Prerequisites

Make sure you have the following installed:

* Python 
* pip or conda
* Git
* Google API key for Gemini
* Tavily API key for web search

---

# How to run the SimpleGPT
## 1. Clone the repository:
   ```bash
   git clone https://github.com/HirdyanshB/SimpleGPT.git
   ```

## 2. Navigate to the project respository:
   ```bash
   cd SimpleGPT
   ```

## 3. Create a virtual environment:
   ```
   python -m venv simplegpt
   ```

## 4. Activate the virtual enviroment:
   ```bash
   simplegpt\Scripts\activate
   ```

## 5. Install the required dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

## 6. Run the application:
   ```bash
   python app.py
   ```

---

## Environment Variables

Create a `.env` file in the project root directory.

```env
GOOGLE_API_KEY=your_google_api_key
GOOGLE_MODEL=gemini-3.5-flash-lite

TAVILY_API_KEY=your_tavily_api_key

LANGSMITH_TRACING=false
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=simplegpt
```

If you do not want to use LangSmith tracing, keep:

```env
LANGSMITH_TRACING=false
```

---

## Run Locally

Start the FastAPI app:

```bash
python app.py
```

The app will be available at:

```text
http://127.0.0.1:8080
```

---

## Project Structure

```text
SimpleGPT/
│
├── app.py                  # FastAPI app and streaming chat endpoints
├── agent.py                # LangGraph agent setup and tool orchestration
├── database.py             # Conversation and persistence logic
├── rag.py                  # Document ingestion and RAG logic
├── tools.py                # Agent tools such as web search, memory, and RAG
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image configuration
├── .dockerignore           # Docker ignore rules
│
├── templates/
│   └── index.html          # Frontend UI
│
├── uploads/                # Uploaded documents
├── data/                   # SQLite database and app data
└── chroma_db/              # ChromaDB vector database storage
```

---

## Docker Deployment

### 1. Build the Docker image

```bash
docker build -t simplegpt .
```

### 2. Run the Docker container

```bash
docker run -d \
  --name simplegpt \
  --restart always \
  -p 8080:8080 \
  --env-file .env \
  simplegpt
```

The app will be available at:

```text
http://localhost:8080
```

---


## Contributing

Contributions are welcome.

To contribute:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

---

## License

This project is open source. Please check the repository license for usage terms.
