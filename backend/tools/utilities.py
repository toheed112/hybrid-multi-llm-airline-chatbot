# utilities.py - Utility tools (user info, Tavily web search)
from dotenv import load_dotenv
import os
load_dotenv()
from tavily import TavilyClient

api_key = os.getenv("TAVILY_API_KEY").strip() if os.getenv("TAVILY_API_KEY") else None
if api_key and api_key.startswith('tvly-'):
    tavily = TavilyClient(api_key=api_key)
else:
    tavily = None

def fetch_user_info(passenger_id):
    """Fetch user bookings."""
    return f"User {passenger_id} has flight LX123."

def search_web(query):
    """Web search via Tavily for live info (or mock)."""
    if tavily is None:
        return "Mock result: No delays reported. (Add TAVILY_API_KEY for live search.)"
    try:
        results = tavily.search(query=query, max_results=3)
        return "\n".join([f"{r['title']}: {r['content'][:150]}..." for r in results['results']])
    except Exception as e:
        return f"Fallback: Search unavailable ({e})."