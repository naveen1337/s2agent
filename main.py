import os
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode, tools_condition
from rich import print as rprint
import httpx

def log_request(request: httpx.Request):
    print("=" * 80)
    print(f">>> {request.method} {request.url}")
    print("Body:")
    rprint(request.content.decode("utf-8", errors="replace"))


def log_response(response: httpx.Response):
    print("=" * 80)
    print(f"<<< {response.status_code} {response.request.url}")


http_client = httpx.Client(
    event_hooks={
        "request": [log_request],
        "response": [log_response],
    },
)

llm = ChatOpenAI(
    # model="ibm-granite/granite-4.0-h-micro",
    model="google/gemini-2.5-flash-lite",   
    api_key=os.environ.get("OR_AGENTDEV_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
    http_client=http_client,
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

SYSTEM_MESSAGE = SystemMessage(
    content="You are a helpful assistant with access to weather tools. Always use the provided weather tools when the user asks about weather conditions or forecasts."
)

def call_llm(state: MessagesState):
    messages = [SYSTEM_MESSAGE] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {
        "messages": [response]
    }

graph = StateGraph(MessagesState)
graph.add_node("llm", call_llm)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, "llm")
graph.add_conditional_edges("llm", tools_condition)
graph.add_edge("tools", "llm")

graph = graph.compile()

res = graph.invoke({"messages": [{"role": "user", "content": "Say hello"}]})
print("Final response:")
print(res.get("messages")[-1].content)
