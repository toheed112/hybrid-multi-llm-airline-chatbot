# backend/agents/primary_assistant.py - Hybrid: OpenAI for tool calling, DeepSeek for response
from dotenv import load_dotenv
import os
load_dotenv()
from openai import OpenAI
import ollama
from datetime import datetime
import json
from backend.tools.flights import search_flights
from backend.tools.policy import lookup_policy
from backend.tools.utilities import search_web
from backend.tools.hotels import search_hotels
from backend.tools.utilities import fetch_user_info

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-llm:7b-chat")

# Define tools for OpenAI (structured calling)
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_flights",
            "description": "Search flights from DB.",
            "parameters": {
                "type": "object",
                "properties": {
                    "departure_airport": {"type": "string"},
                    "arrival_airport": {"type": "string"},
                    "limit": {"type": "integer", "default": 5}
                },
                "required": ["departure_airport"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_policy",
            "description": "Lookup company policies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Web search for live data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_hotels",
            "description": "Search hotels.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"},
                    "checkin": {"type": "string"},
                    "checkout": {"type": "string"}
                },
                "required": ["location"]
            }
        }
    },
    # Add more: book_hotel, etc.
]

def agent(state: dict) -> dict:
    """Agent: OpenAI parses/calls tools, DeepSeek summarizes."""
    history = "\n".join([f"{m['role']}: {m['content']}" for m in state["messages"]])
    user_query = state['messages'][-1]['content']

    # Step 1: OpenAI for tool calling
    messages = [
        {"role": "system", "content": "Call tools for queries. Output function call if needed."},
        {"role": "user", "content": user_query}
    ]
    tool_response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    # Step 2: Execute tool if called
    tool_result = ""
    if tool_response.choices[0].message.tool_calls:
        tool_call = tool_response.choices[0].message.tool_calls[0]
        func_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        if func_name == "search_flights":
            tool_result = search_flights(**args)
        elif func_name == "lookup_policy":
            tool_result = lookup_policy(**args)
        elif func_name == "search_web":
            tool_result = search_web(**args)
        elif func_name == "search_hotels":
            tool_result = search_hotels(**args)
        # Add more tools...
    else:
        tool_result = "No tool needed."

    # Step 3: DeepSeek for natural response
    ollama_prompt = f"System: Summarize tool result naturally.\nTool result: {tool_result}\nUser query: {user_query}\nHistory: {history}\nRespond:"
    ollama_response = ollama.chat(model=OLLAMA_MODEL, messages=[{"role": "user", "content": ollama_prompt}])
    bot_content = ollama_response['message']['content']

    state["messages"].append({"role": "assistant", "content": bot_content})
    return state