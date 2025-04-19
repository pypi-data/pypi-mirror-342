# RAG Server

A FastMCP-based Retrieval-Augmented Generation server for dynamically ingesting public documents and querying them on-the-fly.

## Installation

```bash
pip install -r requirements.txt
```

Ensure you set your OpenAI API key:

```bash
export OPENAI_API_KEY=your_key_here
```

## Running the server

```bash
python -m rag_server.server
```

## API Tools

- ingest_urls(urls: List[str], session_id: Optional[str]) -> session_id
- query_knowledge(session_id: str, question: str) -> answer
