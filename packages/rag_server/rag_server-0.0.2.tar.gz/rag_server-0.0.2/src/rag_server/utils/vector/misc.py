import io
from typing import List

import docx
import requests
import textract
from PyPDF2 import PdfReader
from openai.types import CreateEmbeddingResponse
from rag_server.utils.llm import openai_client, gemini_client

def extract_text_from_url(url: str) -> str:
    """Download the file at the given URL and extract its text."""
    resp = requests.get(url)
    resp.raise_for_status()
    content = resp.content
    ext = url.split(".")[-1].lower()
    if ext == "pdf":
        reader = PdfReader(io.BytesIO(content))
        return "\n".join(p.extract_text() or "" for p in reader.pages)
    elif ext == "docx":
        doc = docx.Document(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs)
    elif ext == "doc":
        return textract.process(io.BytesIO(content), extension="doc").decode("utf-8", errors="ignore")
    else:
        return content.decode("utf-8", errors="ignore")


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into chunks of approximately chunk_size words with overlap."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        chunk = " ".join(words[start: start + chunk_size])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def embed_texts(texts: list[str], retries: int = 3) -> list[list[float]]:
    """Embed a list of texts using OpenAI embeddings with rate limit handling."""
    for attempt in range(retries):
        try:
            # Try text-embedding-3-small first as it's cheaper and newer
            resp: CreateEmbeddingResponse = openai_client.embeddings.create(
                input=texts, 
                model="text-embedding-3-small"
            )
            return [d.embedding for d in resp.data]
        except Exception as e:
            if "too many requests" in str(e).lower() and attempt < retries - 1:
                # If rate limited and not last attempt, wait and retry
                import time
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            elif attempt == retries - 1:
                # On last attempt, fallback to ada-002
                resp: List[List[float]] = gemini_client.embed_documents(
                    texts=texts,
                    task_type="RETRIEVAL_DOCUMENT"
                )
                return resp
            else:
                raise

def get_embedding(text: str, retries: int = 3) -> list[float]:
    """Embed a single text with rate limit handling."""
    return embed_texts([text], retries=retries)[0]
