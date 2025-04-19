import faiss
import numpy as np
import uuid
import chromadb
from chromadb.config import Settings
from rag_server.utils.vector.misc import get_embedding
from concurrent.futures import ThreadPoolExecutor

class EmbeddingAdapter:
    """Adapter to satisfy ChromaDB EmbeddingFunction interface."""
    def __call__(self, input: list[str]) -> list[list[float]]:
        # Use ThreadPoolExecutor for parallel embedding
        with ThreadPoolExecutor() as executor:
            embeddings = list(executor.map(get_embedding, input))
        return embeddings

class VectorStore:
    """Persistent vector store using ChromaDB for storage and FAISS for fast retrieval."""
    def __init__(self, session_id: str, persist_directory: str = "chroma_db", dim: int = 1536):
        self.session_id = session_id
        self.dim = dim
        # Initialize persistent ChromaDB client
        self.chroma_client = chromadb.PersistentClient(path=persist_directory, settings=Settings())
        # Create or open the 'chunks' collection with our embedding function
        self.collection = self.chroma_client.get_or_create_collection(
            name="chunks",
            embedding_function=EmbeddingAdapter()
        )
        # Initialize FAISS HNSW index for fast approx. kNN
        self.index = faiss.index_factory(dim, "HNSW32")
        try:
            self.index.hnsw.efConstruction = 200
            self.index.hnsw.efSearch = 128
        except AttributeError:
            pass
        # Track FAISS IDs and text mapping
        self.ids: list[str] = []
        self.id_to_chunk: dict[str, str] = {}

    def add(self, chunks: list[str]) -> None:
        # Generate unique IDs per chunk
        new_ids = [f"{self.session_id}-{i}-{uuid.uuid4()}" for i in range(len(chunks))]
        
        # Compute embeddings in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            embeddings = list(executor.map(get_embedding, chunks))
        
        # Persist to ChromaDB
        self.collection.add(
            ids=new_ids,
            documents=chunks,
            metadatas=[{"session_id": self.session_id}] * len(chunks),
            embeddings=embeddings
        )
        
        # Add to FAISS index in-memory
        arr = np.array(embeddings, dtype="float32")
        self.index.add(arr)
        
        # Update ID list and mapping in parallel
        def update_mapping(args):
            idx, chunk = args
            self.id_to_chunk[idx] = chunk
            
        self.ids.extend(new_ids)
        with ThreadPoolExecutor() as executor:
            executor.map(update_mapping, zip(new_ids, chunks))

    def search(self, query: str, top_k: int = 5) -> list[str]:
        # On first search, lazy-load all persisted embeddings for this session into FAISS
        if self.index.ntotal == 0:
            # Load this session's embeddings and documents from ChromaDB
            records = self.collection.get(
                where={"session_id": self.session_id},
                include=["embeddings", "documents"],
            )
            emb_list = records.get("embeddings", [])
            # Safely check length of embeddings
            try:
                count = len(emb_list)
            except Exception:
                count = 0
            # Convert to array if there are embeddings, otherwise create empty array
            if count > 0:
                arr = np.array(emb_list, dtype="float32")
            else:
                arr = np.empty((0, self.dim), dtype="float32")
            if arr.shape[0] > 0:
                # Populate FAISS index and ID mapping
                self.index.add(arr)
                # 'ids' and 'documents' are returned by ChromaDB
                self.ids = records["ids"]
                # Update mapping in parallel
                with ThreadPoolExecutor() as executor:
                    executor.map(
                        lambda x: self.id_to_chunk.update({x[0]: x[1]}),
                        zip(records["ids"], records["documents"])
                    )
                
        # If still no data for this session, return empty
        if self.index.ntotal == 0:
            return []
            
        # Compute embedding for the query
        q_emb = np.array([get_embedding(query)], dtype="float32")
        # Retrieve top_k IDs via FAISS
        D, I = self.index.search(q_emb, top_k)
        result_ids = [self.ids[i] for i in I[0]]
        
        # Deduplicate IDs while preserving order to avoid Chroma duplicate errors
        seen = set()
        unique_ids = []
        for rid in result_ids:
            if rid not in seen:
                seen.add(rid)
                unique_ids.append(rid)
                
        if not unique_ids:
            return []
            
        # Fetch documents from ChromaDB
        results = self.collection.get(ids=unique_ids)
        return results["documents"]
