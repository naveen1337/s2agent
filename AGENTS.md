# AGENTS.md

Guidance for AI coding agents working in this repository.

## Project Overview

**s2agent** — a sales & support conversational agent (early prototype).

Currently a single-file LangGraph ReAct-style agent (`main.py`):
- LLM access via `langchain-openai`'s `ChatOpenAI` pointed at **OpenRouter** (`https://openrouter.ai/api/v1`)
- Model: `google/gemini-2.5-flash-lite`, API key read from env var `OR_AGENTDEV_API_KEY`
- Two mock weather tools (`get_current_weather`, `get_weather_forecast`) bound via `ToolNode`
- Graph flow: `START -> llm -> tools_condition -> llm/tools -> END`
- httpx request/response logging hooks print full request bodies to stdout
- Script runs the graph once at import time with a hardcoded "Say hello" message

FastAPI and uvicorn are declared dependencies but not yet used — the intended direction is to serve the graph over HTTP.

## Tech Stack

- Python >= 3.13 (see `.python-version`)
- Package manager: **uv** (`uv.lock` present)
- langgraph, langchain, langchain-openai
- fastapi + uvicorn (planned server layer)
- pydantic v2, python-dotenv, rich (pretty printing), httpx

## Commands

```bash
uv sync                 # install dependencies
uv run main.py          # run the agent script
uv run uvicorn ...      # future: serve via FastAPI (not implemented yet)
```

No tests or linters are configured yet.

## Conventions & Notes

- Single-module layout; keep new nodes/tools in `main.py` until the project warrants splitting into packages.
- Tools use the `@tool` decorator from `langchain_core.tools`; docstrings double as tool descriptions for the LLM.
- State type is LangGraph's built-in `MessagesState`.
- Never hardcode API keys; they come from environment variables (`OR_AGENTDEV_API_KEY`).
- The verbose HTTP logging in `log_request` will dump full payloads (including auth headers context) to stdout — treat it as debug-only and don't enable it in production code paths.
- Model name is currently hardcoded in `main.py`; parameterize if adding configuration.
