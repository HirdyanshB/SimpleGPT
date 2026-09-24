import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv
import certifi

load_dotenv()

# SSL certificate configuration
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver

from tools import tools


# ---------------------------------------------------------
# Directories
# ---------------------------------------------------------

Path("data").mkdir(exist_ok=True)


# ---------------------------------------------------------
# Gemini Models
# ---------------------------------------------------------

# Default model
DEFAULT_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)


# Models supported by this application.
#
# These are current Gemini models suitable for
# general-purpose chat / agentic applications.
ALLOWED_MODELS = {
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
}


# ---------------------------------------------------------
# System Prompt
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are a helpful Agentic AI assistant named SimpleGPT,
similar to ChatGPT.

You can:

1. Answer normal questions.
2. Use tools when needed.
3. Search uploaded documents using the RAG tool.
4. Search the web for latest/current information using Tavily Search.
5. Remember important user information using the memory tool.
6. Recall memory when useful.
7. Use the calculator for mathematical questions.

Rules:

- If the user asks about latest news, current events,
  recent updates, today's information, current prices,
  current people, current versions, new releases,
  or anything time-sensitive, use Tavily Search.

- If the user asks about an uploaded document,
  use search_uploaded_documents.

- If the user asks you to remember something,
  use remember_this.

- If the user asks about previous preferences
  or saved facts, use recall_memory.

- Use calculator for math questions.

- When using web search, summarize the results clearly
  and mention that the answer is based on web search.

- Do not claim information is current unless you have
  verified it using an appropriate tool.

- Be clear, helpful, and concise.
"""


# ---------------------------------------------------------
# Model Validation
# ---------------------------------------------------------

def normalize_model_name(model_name: str | None) -> str:
    """
    Validate the selected model.

    If the frontend does not provide a model, or provides
    an unsupported model, use DEFAULT_MODEL.
    """

    if not model_name:
        return DEFAULT_MODEL

    model_name = model_name.strip()

    if model_name not in ALLOWED_MODELS:
        return DEFAULT_MODEL

    return model_name


# ---------------------------------------------------------
# Build Agent
# ---------------------------------------------------------

def build_agent(model_name: str):
    """
    Build a LangGraph agent using the selected Gemini model.
    """

    selected_model = normalize_model_name(model_name)

    print(f"Starting SimpleGPT with model: {selected_model}")

    # -----------------------------------------------------
    # Gemini LLM
    # -----------------------------------------------------

    llm = ChatGoogleGenerativeAI(
        model=selected_model,
        temperature=0.3,
        streaming=True,
    )

    # Give Gemini access to the application's tools
    llm_with_tools = llm.bind_tools(tools)

    # -----------------------------------------------------
    # Chatbot Node
    # -----------------------------------------------------

    def chatbot_node(state: MessagesState):
        messages = [
            SystemMessage(content=SYSTEM_PROMPT)
        ] + state["messages"]

        response = llm_with_tools.invoke(messages)

        return {
            "messages": [response]
        }

    # -----------------------------------------------------
    # Tool Node
    # -----------------------------------------------------

    tool_node = ToolNode(tools)

    # -----------------------------------------------------
    # LangGraph Workflow
    # -----------------------------------------------------

    workflow = StateGraph(MessagesState)

    workflow.add_node(
        "chatbot",
        chatbot_node
    )

    workflow.add_node(
        "tools",
        tool_node
    )

    workflow.add_edge(
        START,
        "chatbot"
    )

    workflow.add_conditional_edges(
        "chatbot",
        tools_condition
    )

    workflow.add_edge(
        "tools",
        "chatbot"
    )

    # -----------------------------------------------------
    # SQLite Checkpointer
    # -----------------------------------------------------

    conn = sqlite3.connect(
        "data/langgraph_checkpoints.sqlite",
        check_same_thread=False
    )

    checkpointer = SqliteSaver(conn)

    # -----------------------------------------------------
    # Compile Graph
    # -----------------------------------------------------

    return workflow.compile(
        checkpointer=checkpointer
    )


# ---------------------------------------------------------
# Agent Cache
# ---------------------------------------------------------

_AGENT_CACHE = {}


def get_agent(model_name: str | None = None):
    """
    Return a cached LangGraph agent for the selected model.

    Agents are created only once per model and then reused.
    """

    selected_model = normalize_model_name(model_name)

    if selected_model not in _AGENT_CACHE:
        _AGENT_CACHE[selected_model] = build_agent(
            selected_model
        )

    return _AGENT_CACHE[selected_model]
