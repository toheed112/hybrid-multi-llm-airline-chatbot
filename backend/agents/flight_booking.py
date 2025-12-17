# backend/agents/flight_booking.py - Specialized flight agent
from dotenv import load_dotenv
import os
load_dotenv()
from openai import OpenAI
import ollama
from datetime import datetime
import json
from backend.tools.flights import search_flights, update_ticket_to_new_flight
from backend.tools.policy import lookup_policy
from backend.tools.utilities import search_web
from backend.tools.utilities import fetch_user_info

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-llm:7b-chat")

# Flight-specific tools for OpenAI
flight_tools = [
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
            "name": "update_ticket_to_new_flight",
            "description": "Update ticket to new flight.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_no": {"type": "string"},
                    "new_flight_id": {"type": "integer"},
                    "passenger_id": {"type": "string"}
                },
                "required": ["ticket_no", "new_flight_id", "passenger_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search for live flight delays or updates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
]

def flight_assistant(state: dict) -> dict:
    """Flight expert assistant: OpenAI calls flight tools, DeepSeek summarizes."""
    history = "\n".join([f"{m['role']}: {m['content']}" for m in state["messages"]])
    user_query = state['messages'][-1]['content']

    # Step 1: OpenAI for flight tool calling
    messages = [
        {"role": "system", "content": "You are a flight expert. Call tools for searches/updates. Output function call if needed."},
        {"role": "user", "content": user_query}
    ]
    tool_response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=flight_tools,
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
        elif func_name == "update_ticket_to_new_flight":
            tool_result = update_ticket_to_new_flight(**args)
        elif func_name == "search_web":
            tool_result = search_web(**args)
    else:
        tool_result = "No flight tool needed."

    # Step 3: DeepSeek for natural flight response
    ollama_prompt = f"System: As a flight expert, summarize tool result naturally.\nTool result: {tool_result}\nUser query: {user_query}\nHistory: {history}\nRespond:"
    ollama_response = ollama.chat(model=OLLAMA_MODEL, messages=[{"role": "user", "content": ollama_prompt}])
    bot_content = ollama_response['message']['content']

    state["messages"].append({"role": "assistant", "content": bot_content})
    return state