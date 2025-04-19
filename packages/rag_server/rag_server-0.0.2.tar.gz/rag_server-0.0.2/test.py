import pytest
from rag_server.server import ingest_urls, query_knowledge

def test_ingest_urls():
    # Test with a single URL
    session_id = ingest_urls(["https://example.com/test.pdf"])
    assert isinstance(session_id, str)
    assert len(session_id) > 0

    # Test with multiple URLs and explicit session_id
    explicit_id = "test-session"
    returned_id = ingest_urls(
        ["https://example.com/doc1.pdf", "https://example.com/doc2.docx"],
        session_id=explicit_id
    )
    assert returned_id == explicit_id

def test_query_knowledge():
    # First ingest some test documents
    session_id = ingest_urls(["https://example.com/test.pdf"])
    
    # Test querying the knowledge base
    response = query_knowledge(session_id, "What is this document about?")
    assert isinstance(response, str)
    assert len(response) > 0

    # Test with non-existent session
    response = query_knowledge("non-existent-session", "test question")
    assert isinstance(response, str)
    # Should return empty context when no documents found
    assert response == ""
