import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def build_index():
    """
    Builds a vector index from chunks.json
    """

    with open("chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)

    texts = [chunk["chunk"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    faiss.write_index(index, "vector.index")

    print(f"Indexed {len(chunks)} chunks")

    return index, chunks


def load_index():
    """
    Loads an existing vector index
    """

    with open("chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)

    index = faiss.read_index("vector.index")

    return index, chunks


def retrieve(query, index, chunks, top_k=3):
    """
    Semantic search
    """

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    # FAISS returns a 2D array for a single query: shape (1, top_k).
    # Flatten it so each idx is a scalar integer.
    indices = indices[0]

    results = []

    for idx in indices:
        results.append(
            {
                "chunk": chunks[int(idx)]["chunk"],
                "metadata": chunks[int(idx)]["metadata"]
            }
        )

    return results


if __name__ == "__main__":

    # Rebuild index from scratch
    index, chunks = build_index()

    test_queries = [
        "password security",
        "employee attendance",
        "machine learning",
        "company policy",
        "customer information protection"
    ]

    for query in test_queries:

        print("\n" + "=" * 60)
        print(f"QUERY: {query}")
        print("=" * 60)

        results = retrieve(
            query=query,
            index=index,
            chunks=chunks,
            top_k=3
        )

        for i, result in enumerate(results, start=1):

            print(f"\nResult #{i}")

            print(
                f"Source: {result['metadata']['source']}"
            )

            print(
                f"Page: {result['metadata']['page']}"
            )

            print(
                f"Chunk ID: {result['metadata']['chunk_id']}"
            )

            print(
                f"Text: {result['chunk']}"
            )