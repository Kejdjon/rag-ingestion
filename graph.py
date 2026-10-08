from typing import TypedDict
from langgraph.graph import StateGraph
import asyncio
from mcp_client import get_employee_from_mcp

from rag import (
    load_resource,
    retrieve,
    build_context,
    generate_answer
)

# Load RAG resources once
index, chunks = load_resource()

# Mock customer database
CUSTOMERS = {
    "1001": {
        "name": "John Smith",
        "status": "Active"
    },
    "1002": {
        "name": "Jane Doe",
        "status": "Suspended"
    }
}


class AgentState(TypedDict, total=False):
    question: str
    tool: str
    rewritten_question: str
    context: str
    answer: str
    citation: str
    score: float
    status: str


# --------------------
# TOOLS
# --------------------

def calculator_tool(expression: str):

    try:
        result = eval(expression)

        return {
            "success": True,
            "result": result
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


def customer_lookup_tool(customer_id: str):

    customer = CUSTOMERS.get(customer_id)

    if customer:

        return {
            "success": True,
            "customer": customer
        }

    return {
        "success": False,
        "error": "Customer not found"
    }
def error_node(state):

    return {
        "status": "error",
        "answer": (
            "I cannot process this request "
            "at the moment."
        ),
        "citation": "Error Handler"
    }

    

# --------------------
# ROUTER NODE
# --------------------

def router_node(state):

    question = state["question"].lower()

    if any(op in question for op in ["+", "-", "*", "/"]):

        tool = "calculator"

    elif "customer" in question:

        tool = "customer"

    elif "employee" in question:

        tool = "mcp"

    else:

        tool = "rag"

    print("\n=== Router Node ===")
    print(f"Selected Tool: {tool}")

    return {
        "tool": tool
    }

# --------------------
# CALCULATOR NODE
# --------------------

def calculator_node(state):

    result = calculator_tool(
        state["question"]
    )

    if result["success"]:

        return {
            "status": "success",
            "answer":
                f"Result = {result['result']}",
            "citation":
                "Calculator Tool"
        }

    return {
        "status": "error",
        "answer":
            "Invalid mathematical expression.",
        "citation":
            "Calculator Tool"
    }



# --------------------
# CUSTOMER NODE
# --------------------
def customer_node(state):

    customer_id = "".join(
        c for c in state["question"]
        if c.isdigit()
    )

    result = customer_lookup_tool(
        customer_id
    )

    if result["success"]:

        customer = result["customer"]

        return {
            "status": "success",
            "answer":
                f"Customer: {customer['name']} | "
                f"Status: {customer['status']}",
            "citation":
                "Customer Lookup Tool"
        }

    return {
        "status": "error",
        "answer":
            "Customer not found",
        "citation":
            "Customer Lookup Tool"
    }

# --------------------
# MCP NODE
# --------------------
def mcp_node(state):

    employee_id = "".join(
        c for c in state["question"]
        if c.isdigit()
    )

    try:

        result = asyncio.run(
            get_employee_from_mcp(
                employee_id
            )
        )

        return {
            "status": "success",
            "answer": str(result),
            "citation": "MCP Server"
        }

    except Exception:

        return {
            "status": "error",
            "answer": "MCP server unavailable",
            "citation": "MCP Server"
        }
# --------------------
# RAG NODES
# --------------------

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

    context = build_context(
        retrieved
    )

    citation = "None"

    if retrieved:

        citation = (
            retrieved[0]["metadata"]["source"]
        )

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

        return {
            "status": "error",
            "answer":
                (
                    "I cannot find enough "
                    "evidence in the provided "
                    "documents."
                ),
            "citation":
                "None"
        }

    print("\n=== Generate Node ===")
    print(answer)

    return {
        "status": "success",
        "answer": answer
    }


# --------------------
# OUTPUT NODE
# --------------------

def output_node(state):

    print("\nAnswer:")
    print("=" * 60)
    print(state["answer"])

    print("\nCitation")
    print("=" * 60)
    print(state["citation"])

    return {}


# --------------------
# ROUTING
# --------------------

def route_tool(state):

    return state["tool"]


# --------------------
# BUILD GRAPH
# --------------------

graph_builder = StateGraph(
    AgentState
)

graph_builder.add_node(
    "router",
    router_node
)

graph_builder.add_node(
    "calculator",
    calculator_node
)

graph_builder.add_node(
    "customer",
    customer_node
)
graph_builder.add_node(
    "mcp",
    mcp_node
)

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
graph_builder.add_node(
    "error",
    error_node
)

graph_builder.set_entry_point(
    "router"
)

graph_builder.add_conditional_edges(
    "router",
    route_tool,
    {
        "calculator": "calculator",
        "customer": "customer",
        "mcp": "mcp",
        "rag": "rewrite"
    }
)

graph_builder.add_edge(
    "calculator",
    "output"
)

graph_builder.add_edge(
    "customer",
    "output"
)
graph_builder.add_edge(
    "mcp",
    "output"
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

graph = graph_builder.compile()




if __name__ == "__main__":

    print("LangGraph Multi-Tool Assistant")

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