import io

import docx
import requests
import textract
from PyPDF2 import PdfReader
from openai.types import CreateEmbeddingResponse

from rag_server.utils.llm import openai_client


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


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a list of texts using OpenAI embeddings."""
    resp : CreateEmbeddingResponse = openai_client.embeddings.create(input=texts, model="text-embedding-ada-002")
    return [d.embedding for d in resp.data]

def get_embedding(text: str) -> list[float]:
    """Embed a single text."""
    resp : CreateEmbeddingResponse = openai_client.embeddings.create(input=text, model="text-embedding-ada-002")
    return resp.data[0].embedding
