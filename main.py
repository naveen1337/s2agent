import os
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, MessagesState, START, END, add_messages
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.prebuilt import ToolNode, tools_condition
from rich import print as rprint
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

conn = sqlite3.connect(
    "checkpoints.sqlite",
    check_same_thread=False
)

llm = ChatOpenAI(
    model="google/gemini-2.5-flash-lite",   
    api_key=os.environ.get("OR_AGENTDEV_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)

@tool
def get_current_weather(location: str) -> str:
    """Get the current weather for a given location."""
    return f"The weather in {location} is sunny and 22°C."

@tool
def get_weather_forecast(location: str, days: int = 3) -> str:
    """Get the weather forecast for a given location for a number of days."""
    return f"The {days}-day forecast for {location}: sunny, high of 24°C, low of 15°C."

tools = [get_current_weather, get_weather_forecast]
llm_with_tools = llm.bind_tools(tools)


class MyAppState(TypedDict):
    env_version: str = "1.0.0"
    user_id: str = None
    app_session_id: str = "0000"
    messages: Annotated[list, add_messages]
    llm_count: int = 0

def call_llm(state: MyAppState):
    messages = state["messages"]
    llm_count = state.get("llm_count", 0)
    print(f"LLM call count: {llm_count}")
    if (llm_count > 1):
        return "You have reached the maximum number of LLM calls allowed in this session."
    response = llm_with_tools.invoke(messages)
    if hasattr(response, "response_metadata"):
        md = response.response_metadata
        tu = md.get("token_usage") or {}
        response.response_metadata = {
            "finish_reason": md.get("finish_reason"),
            "model_name": md.get("model_name"),
            "total_tokens": tu.get("total_tokens"),
            "prompt_tokens": tu.get("prompt_tokens"),
        }
    return {
        "messages": [response],
        "llm_count": state.get("llm_count", 0) + 1
    }

graph = StateGraph(MyAppState)

def init_state(state: MyAppState):
    state["env_version"] = "1.0.0"
    state["messages"] = []
    return state

# init node needed to set the state. so langgraph can read that
graph.add_node("init", init_state)
graph.add_node("llm", call_llm)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, "init")
graph.add_edge("init", "llm")
graph.add_conditional_edges("llm", tools_condition)
graph.add_edge("tools", "llm")

checkpointer = SqliteSaver(conn)
config = {
    "configurable": {
        "thread_id": "user-004"
    }
}

messages = [
    SystemMessage(content="You are a helpful assistant.", id="system"),
    HumanMessage(content="What is my name?", id="user")
]


graph = graph.compile(checkpointer=checkpointer)
# Set the state to the initial state
res = graph.invoke({"messages": messages, "user_id": "nav", "llm_count": 2}, config=config)
rprint(res.get("messages")[-1].content)

# Read the state
state = graph.get_state(config=config)
rprint(state)

# checkpoint_tuple = checkpointer.get_tuple(config)
# rprint(checkpoint_tuple)
# res2 = graph.invoke({"messages": [{"role": "user", "content": "What is my name?"}]}, config=config)
# rprint(res2.get("messages")[-1].content) 
