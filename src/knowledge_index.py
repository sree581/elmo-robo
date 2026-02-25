import os
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# Load embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def load_documents():
    base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    docs = []

    for file in os.listdir(base_path):
        file_path = os.path.join(base_path, file)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

            # Split by double newline (paragraph level)
            chunks = content.split("\n\n")

            for chunk in chunks:
                clean_chunk = chunk.strip()
                if clean_chunk:
                    docs.append(clean_chunk)

    return docs


documents = load_documents()
embeddings = embed_model.encode(documents)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

def retrieve(query, top_k=4):
    query_embedding = embed_model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)
    return [documents[i] for i in indices[0]]
