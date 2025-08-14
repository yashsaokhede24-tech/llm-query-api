import faiss
from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingSearch:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.clauses = []

    def index_document(self, text: str):
        self.clauses = [c.strip() for c in text.split('.') if c.strip()]
        embeddings = self.model.encode(self.clauses)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

    def retrieve(self, query: str, top_k=5) -> List[str]:
        query_emb = self.model.encode([query])
        _, I = self.index.search(query_emb, top_k)
        return [self.clauses[i] for i in I[0]]