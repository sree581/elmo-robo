import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class RetrievalEngine:
    def __init__(self, knowledge_path):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.documents = self.load_knowledge(knowledge_path)
        self.index = self.build_index(self.documents)

    def load_knowledge(self, path):
        with open(path, "r") as f:
            text = f.read()
        return text.split("\n")

    def build_index(self, documents):
        embeddings = self.model.encode(documents)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings))
        return index

    def search(self, query, k=3):
        query_vector = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_vector), k)
        return [self.documents[i] for i in indices[0]]