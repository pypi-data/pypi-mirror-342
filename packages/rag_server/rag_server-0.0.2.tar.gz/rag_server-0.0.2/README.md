# RAG Server

A FastMCP-based Retrieval-Augmented Generation server for dynamically ingesting public documents and querying them on-the-fly. This server implements the Model Context Protocol (MCP) to enable seamless integration between AI models and external data sources.

## Features

- Document ingestion from public URLs (PDF, DOCX, DOC)
- Hybrid vector search using both OpenAI and Google Gemini embeddings
- Session-based context management via MCP
- Automatic fallback and retry mechanisms for embedding generation
- Support for chunking and overlapping text segments

## Installation

```
uv pip install -e .
```

## Tools

The server exposes the following MCP tools defined in `src/rag_server/server.py`:

### `ingest_urls`

**Description**: Ingest a list of public URLs (PDF, DOCX, DOC) into an ephemeral session. Returns a `session_id` for querying. You can pass an existing `session_id` to ingest into a specific session.

**Signature**: `ingest_urls(urls: list[str], session_id: Optional[str] = None) -> str`

- `urls`: List of public document URLs to ingest.
- `session_id` _(optional)_: Existing session identifier.

### `query_knowledge`

**Description**: Query the ingested documents in the given session using RAG. Returns a generated answer.

**Signature**: `query_knowledge(session_id: str, question: str) -> str`

- `session_id`: Session identifier where documents were ingested.
- `question`: The question to query against ingested documents.

