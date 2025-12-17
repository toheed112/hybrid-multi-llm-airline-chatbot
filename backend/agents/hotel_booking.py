# hotel_booking.py - Specialized hotel booking agent
from dotenv import load_dotenv
import os
load_dotenv()
from openai import OpenAI
import ollama
from datetime import datetime
import json
from backend.tools.hotels import search_hotels, book_hotel
from backend.tools.policy import lookup_policy
from backend.tools.utilities import search_web
from backend.tools.utilities import fetch_user_info

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-llm:7b-chat")

# Hotel-specific tools for OpenAI
hotel_tools = [
    {
        "type": "function",
        "function": {
            "name": "search_hotels",
            "description": "Search hotels from DB.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"},
                    "checkin": {"type": "string"},
                    "checkout": {"type": "string"},
                    "limit": {"type": "integer", "default": 5}
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_hotel",
            "description": "Book a hotel.",
            "parameters": {
                "type": "object",
                "properties": {
                    "hotel_id": {"type": "integer"},
                    "passenger_id": {"type": "string"}
                },
                "required": ["hotel_id", "passenger_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search for live hotel availability or reviews.",
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

def hotel_assistant(state: dict) -> dict:
    """Hotel booking expert: OpenAI calls hotel tools, DeepSeek summarizes."""
    history = "\n".join([f"{m['role']}: {m['content']}" for m in state["messages"]])
    user_query = state['messages'][-1]['content']

    # Step 1: OpenAI for hotel tool calling
    messages = [
        {"role": "system", "content": "You are a hotel booking expert. Call tools for searches/bookings. Output function call if needed."},
        {"role": "user", "content": user_query}
    ]
    tool_response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=hotel_tools,
        tool_choice="auto"
    )

    # Step 2: Execute tool if called
    tool_result = ""
    if tool_response.choices[0].message.tool_calls:
        tool_call = tool_response.choices[0].message.tool_calls[0]
        func_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        if func_name == "search_hotels":
            tool_result = search_hotels(**args)
        elif func_name == "book_hotel":
            tool_result = book_hotel(**args)
        elif func_name == "search_web":
            tool_result = search_web(**args)
    else:
        tool_result = "No hotel tool needed."

    # Step 3: DeepSeek for natural hotel response
    ollama_prompt = f"System: As a hotel expert, summarize tool result naturally.\nTool result: {tool_result}\nUser query: {user_query}\nHistory: {history}\nRespond:"
    ollama_response = ollama.chat(model=OLLAMA_MODEL, messages=[{"role": "user", "content": ollama_prompt}])
    bot_content = ollama_response['message']['content']

    state["messages"].append({"role": "assistant", "content": bot_content})
    return state