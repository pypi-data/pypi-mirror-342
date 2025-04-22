from datetime import datetime

from app.config import settings
from app.core.llm import get_llm
from app.rag.models import State
from app.rag.nodes import Assistant
from app.rag.tools import create_tool_node_with_fallback, get_all_tools
from app.utils.logging import logger
from app.utils.prompts import system_prompt_template
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition


def build_rag_graph(model_name: str = None):
    """Build and return the RAG graph."""
    logger.info(f"Building RAG graph with model: {model_name or settings.LLM_MODEL}")

    system_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt_template),
            ("placeholder", "{messages}"),
        ]
    ).partial(time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    llm = get_llm(model_name)
    tools = get_all_tools()

    assistant_runnable = system_prompt | llm.bind_tools(tools)

    builder = StateGraph(State)

    # Define the nodes: these to do the work
    builder.add_node("assistant", Assistant(assistant_runnable))
    builder.add_node("tools", create_tool_node_with_fallback(tools))

    # Define the edges: these determine the flow of the graph
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")

    graph = builder.compile()

    logger.info("RAG graph built successfully")

    return graph
