from functools import lru_cache

from langgraph.graph import END, START, StateGraph

from .nodes import (
    context_injection_node,
    conversation_node,
    summarize_conversation_node
)
from .state import AICompanionState
from .edges import should_summarize_conversation


@lru_cache(maxsize=1)
def create_workflow_graph():
    graph_builder = StateGraph(AICompanionState)

    # Add all nodes
    graph_builder.add_node("context_injection_node", context_injection_node)
    graph_builder.add_node("conversation_node", conversation_node)
    graph_builder.add_node("summarize_conversation_node", summarize_conversation_node)


    # Define the flow
    graph_builder.add_edge(START, "context_injection_node")
    graph_builder.add_edge("context_injection_node", "conversation_node")

    graph_builder.add_conditional_edges("conversation_node", should_summarize_conversation)

    graph_builder.add_edge("summarize_conversation_node", END)

    return graph_builder


# Compiled without a checkpointer. Used for LangGraph Studio
graph = create_workflow_graph().compile()