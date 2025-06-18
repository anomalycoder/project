import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from app.utils import load_course_content, load_discourse_posts
import json
# Ensure output dir exists
os.makedirs("vectorstore", exist_ok=True)

# Load and combine data
course_text = load_course_content()
discourse_text = load_discourse_posts()
documents = (course_text + "\n\n" + discourse_text).split("\n\n")

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(documents, convert_to_numpy=True)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save
faiss.write_index(index, "vectorstore/index.faiss")
with open("vectorstore/chunks.json", "w", encoding="utf-8") as f:
    json.dump(documents, f, indent=2)

def get_relevant_chunks(query, top_k=5):
    query_embedding = model.encode([query], convert_to_numpy=True)
    index = faiss.read_index("vectorstore/index.faiss")
    distances, indices = index.search(query_embedding, top_k)

    with open("vectorstore/chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)

    return [chunks[i] for i in indices[0] if i < len(chunks)]
