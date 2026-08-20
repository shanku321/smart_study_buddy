import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

dimension = 384

index = faiss.IndexFlatL2(dimension)

documents = []


def add_document(text):

    embedding = model.encode([text])

    index.add(
        np.array(
            embedding,
            dtype="float32"
        )
    )

    documents.append(text)


def search(query):

    query_vector = model.encode([query])

    D, I = index.search(
        np.array(
            query_vector,
            dtype="float32"
        ),
        3
    )

    results = []

    for idx in I:
        if idx < len(documents):
            results.append(documents[idx])

    return results