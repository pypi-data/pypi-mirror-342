import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from rag_server.utils.vector.misc import get_embedding, embed_texts


class VectorStore:
    """Simple in-memory vector store using FAISS."""
    def __init__(self, dim: int = 1536):
        self.dim = dim
        # Use an HNSW approximate nearest neighbor index (no training needed)
        self.index = faiss.index_factory(dim, "HNSW32")
        # Configure HNSW parameters for construction and search quality
        try:
            self.index.hnsw.efConstruction = 200
            self.index.hnsw.efSearch = 128
        except AttributeError:
            pass
        self.texts: list[str] = []
        # Initialize TF-IDF vectorizer and matrix
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None

    def add(self, chunks: list[str]) -> None:
        embeddings = embed_texts(chunks)
        arr = np.array(embeddings, dtype="float32")
        self.index.add(arr)
        self.texts.extend(chunks)
        # Update TF-IDF matrix
        self.tfidf_matrix = self.vectorizer.fit_transform(self.texts)

    def search(self, query: str, top_k: int = 5, alpha: float = 0.5) -> list[str]:
        """Perform hybrid search combining semantic (FAISS) and lexical (TF-IDF) scores."""
        # Semantic search via FAISS
        q_emb = np.array([get_embedding(query)], dtype="float32")
        D, I = self.index.search(q_emb, top_k)
        vect_ids = I[0].tolist()
        vect_scores = [-d for d in D[0]]
        # Lexical search via TF-IDF
        if self.tfidf_matrix is None:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.texts)
        q_tfidf = self.vectorizer.transform([query])
        tfidf_scores_all = q_tfidf.dot(self.tfidf_matrix.T).toarray()[0]
        tfidf_top = np.argsort(-tfidf_scores_all)[:top_k].tolist()
        # Combine candidate document indices
        candidate_ids = set(vect_ids + tfidf_top)
        vect_min = min(vect_scores) if vect_scores else 0.0
        scores = []
        for idx in candidate_ids:
            vs = vect_scores[vect_ids.index(idx)] if idx in vect_ids else vect_min
            ts = float(tfidf_scores_all[idx])
            scores.append((idx, vs, ts))
        # Normalize and blend scores
        vs_vals = [v for _, v, _ in scores]
        ts_vals = [t for _, _, t in scores]
        vmin, vmax = min(vs_vals), max(vs_vals)
        tmin, tmax = min(ts_vals), max(ts_vals)
        blended = []
        for idx, vs, ts in scores:
            vn = (vs - vmin) / (vmax - vmin) if vmax > vmin else 0.0
            tn = (ts - tmin) / (tmax - tmin) if tmax > tmin else 0.0
            combined = alpha * vn + (1 - alpha) * tn
            blended.append((idx, combined))
        # Sort by blended score and return top_k chunks
        top = sorted(blended, key=lambda x: x[1], reverse=True)[:top_k]
        return [self.texts[i] for i, _ in top]
