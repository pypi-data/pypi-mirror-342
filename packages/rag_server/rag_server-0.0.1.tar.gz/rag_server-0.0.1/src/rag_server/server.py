# server.py
import uuid
from typing import Optional

from fastmcp import FastMCP

from rag_server.utils.vector.misc import chunk_text, extract_text_from_url
from rag_server.utils.vector.store import VectorStore

# Initialize the MCP server
mcp = FastMCP(name="syne_rag_server", instructions= "You are a helpful assistant that can answer questions about the documents in the session.")

# In-memory sessions: mapping session_id -> VectorStore
_sessions = {}

@mcp.tool(
    description="Ingest a list of public URLs (PDF, DOCX, DOC) into an ephemeral session. Returns a session_id to use for querying. You can pass in a session_id to ingest into a specific session."
)
def ingest_urls(urls: list[str], session: Optional[str] = None) -> str:
    """
    Ingest a list of public URLs (PDF, DOCX, DOC) into an ephemeral session.
    Returns a session_id to use for querying.
    """
    session_id = str(uuid.uuid4() if session is None else session)
    vs = VectorStore()
    for url in urls:
        text = extract_text_from_url(url)
        chunks = chunk_text(text)
        vs.add(chunks)
    _sessions[session_id] = vs
    return session_id

@mcp.tool(
    description="Query the ingested documents in the given session using RAG. Returns a generated answer."
)
def query_knowledge(session_id: str, question: str) -> str:
    """
    Query the ingested documents in the given session using RAG.
    Returns a generated answer.
    """
    vs = _sessions.get(session_id)
    if not vs:
        return f"Session ID {session_id} not found. Please call ingest_urls first."
    docs = vs.search(question)
    context = "\n\n".join(docs)
    return context

def main():
    # Run the server
    mcp.run()