import json
import faiss
from sentence_transformers import SentenceTransformer
from transformers import pipeline

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)


def load_resource():

    with open(
        "chunks.json",
        "r",
        encoding="utf-8"
    ) as f:
        chunks = json.load(f)

    index = faiss.read_index("vector.index")

    return index, chunks


def retrieve(query, index, chunks, top_k=1):

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for idx in indices[0]:
        results.append(chunks[idx])

    return results, distances[0][0]


def build_context(results):

    context = "\n\n".join(
        r["chunk"]
        for r in results
    )

    return context


def generate_answer(question, context):

    prompt = f"""
Context:
{context}

Question:
{question}

Give a short answer based only on the context.
"""

    response = generator(
        prompt,
        max_length=50,
        do_sample=False
    )

    answer = response[0]["generated_text"].strip()

    return answer


def rag(question):

    index, chunks = load_resource()

    retrieved, score = retrieve(
        question,
        index,
        chunks,
        top_k=1
    )

    context = build_context(retrieved)

    answer = generate_answer(
        question,
        context
    )

    if not answer or score > 1.5:

        print("\nAnswer:")
        print("=" * 60)
        print("I cannot find enough evidence in the provided documents.")

        print("\nSources")
        print("=" * 60)
        print("None")

        return

    print("\nAnswer:")
    print("=" * 60)
    print(answer)

    print("\nSources")
    print("=" * 60)

    for source in retrieved:
        print(source["metadata"]["source"])


if __name__ == "__main__":

    while True:

        question = input(
            "\nEnter your question(q to quit): "
        )

        if question.lower() == "q":
            break

        rag(question)