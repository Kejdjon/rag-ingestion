from typing import TypedDict
from langgraph.graph import StateGraph

from rag import (
    load_resource,
    retrieve,
    build_context,
    generate_answer
)


# Load resources once
index, chunks = load_resource()


class RAGState(TypedDict):
    question: str
    rewritten_question: str
    context: str
    answer: str
    citation: str
    score: float


def rewrite_node(state):

    question = state["question"]

    replacements = {
        "ai": "artificial intelligence",
        "ml": "machine learning",
        "staff": "employees",
        "security breach": "security incident"
    }

    rewritten = question.lower()

    for old, new in replacements.items():
        rewritten = rewritten.replace(old, new)

    print("\n=== Rewrite Node ===")
    print(f"Original: {question}")
    print(f"Rewritten: {rewritten}")

    return {
        "rewritten_question": rewritten
    }


def retrieve_node(state):

    query = state["rewritten_question"]

    retrieved, score = retrieve(
        query,
        index,
        chunks,
        top_k=1
    )

    context = build_context(retrieved)

    citation = "None"

    if retrieved:
        citation = retrieved[0]["metadata"]["source"]

    print("\n=== Retrieve Node ===")
    print(f"Citation: {citation}")
    print(f"Similarity Score: {score}")

    return {
        "context": context,
        "citation": citation,
        "score": score
    }


def generate_node(state):

    score = state["score"]

    answer = generate_answer(
        state["question"],
        state["context"]
    )

    if (
        not answer
        or answer.lower() == "unanswerable"
        or score > 1.5
    ):
        answer = (
            "I cannot find enough evidence "
            "in the provided documents."
        )

        return {
            "answer": answer,
            "citation": "None"
        }

    print("\n=== Generate Node ===")
    print(answer)

    return {
        "answer": answer
    }


def output_node(state):

    print("\nAnswer:")
    print("=" * 60)
    print(state["answer"])

    print("\nCitation")
    print("=" * 60)
    print(state["citation"])

    return {}


# Build Graph

graph_builder = StateGraph(RAGState)

graph_builder.add_node(
    "rewrite",
    rewrite_node
)

graph_builder.add_node(
    "retrieve",
    retrieve_node
)

graph_builder.add_node(
    "generate",
    generate_node
)

graph_builder.add_node(
    "output",
    output_node
)


# Define Flow

graph_builder.set_entry_point(
    "rewrite"
)

graph_builder.add_edge(
    "rewrite",
    "retrieve"
)

graph_builder.add_edge(
    "retrieve",
    "generate"
)

graph_builder.add_edge(
    "generate",
    "output"
)


# Compile Graph

graph = graph_builder.compile()


if __name__ == "__main__":

    print("LangGraph RAG Assistant")

    while True:

        question = input(
            "\nEnter your question (q to quit): "
        )

        if question.lower() == "q":
            break

        graph.invoke(
            {
                "question": question
            }
        )