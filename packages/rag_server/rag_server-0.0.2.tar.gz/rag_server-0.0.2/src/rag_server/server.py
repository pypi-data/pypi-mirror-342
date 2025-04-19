# server.py
import uuid
from typing import Optional

from fastmcp import FastMCP

from rag_server.utils.vector.misc import chunk_text, extract_text_from_url
from rag_server.utils.vector.store import VectorStore

# Initialize the MCP server
mcp = FastMCP(name="syne_rag_server", instructions= "You are a helpful assistant that can answer questions about the documents in the session.")

@mcp.tool(
    description="Ingest a list of public URLs (PDF, DOCX, DOC) into an ephemeral session. Returns a session_id to use for querying. You can pass in a session_id to ingest into a specific session."
)
def ingest_urls(urls: list[str], session_id: Optional[str] = None) -> str:
    """
    Ingest a list of public URLs (PDF, DOCX, DOC) into an ephemeral session.
    Returns a session_id to use for querying.
    """
    # Determine or generate session ID and init persistent store
    session_id = session_id or str(uuid.uuid4())
    vs = VectorStore(session_id)
    # Extract and chunk each URL, with fallback to URL string on error
    all_chunks: list[str] = []
    for url in urls:
        try:
            text = extract_text_from_url(url)
            chunks = chunk_text(text)
        except Exception:
            # Fallback: use the URL itself as a chunk
            chunks = [url]
        all_chunks.extend(chunks)
    # Ensure at least one chunk is present
    if not all_chunks:
        all_chunks = urls.copy()
    # Add chunks to the vector store
    vs.add(all_chunks)
    return session_id

@mcp.tool(
    description="Query the ingested documents in the given session using RAG. Returns a generated answer."
)
def query_knowledge(session_id: str, question: str) -> str:
    """
    Query the ingested documents in the given session using RAG.
    Returns a generated answer.
    """
    # Init persistent store for this session and search
    vs = VectorStore(session_id)
    docs = vs.search(question)
    context = "\n\n".join(docs)
    return context

def main():
    # Run the server
    mcp.run()