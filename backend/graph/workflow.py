# workflow.py - Pure Python simulation of LangGraph flow (Parts 1-4)
from typing import Dict, List
from typing_extensions import TypedDict
from backend.agents.primary_assistant import agent
from backend.tools.utilities import fetch_user_info
from backend.tools import SENSITIVE_TOOLS

class State(TypedDict):
    messages: List[Dict]
    user_info: str
    passenger_id: str
    interrupt: bool

def route_tools(state: Dict) -> str:
    last_msg = state["messages"][-1]
    if not last_msg.get("tool_calls"):
        return "end"
    tool_name = last_msg["tool_calls"][0]["name"]
    return "sensitive" if tool_name in SENSITIVE_TOOLS else "safe"

def execute_tools(state: Dict, tool_type: str) -> Dict:
    tool_calls = state["messages"][-1]["tool_calls"]
    for tc in tool_calls:
        if tool_type == "sensitive":
            state["interrupt"] = True
            break
        else:
            func_name = tc["name"]
            args = tc["args"]
            try:
                func = globals()[func_name]
                result = func(**args)
            except Exception as e:
                result = f"Tool error: {e}"
            state["messages"].append({"role": "tool", "content": str(result)})
    return state

def run_graph_v4(input_msg: str, config: Dict, history: List = None) -> List:
    if history is None:
        history = []
    state: State = {
        "messages": history + [{"role": "user", "content": input_msg}],
        "user_info": fetch_user_info(config["passenger_id"]),
        "passenger_id": config["passenger_id"],
        "interrupt": False
    }
    
    # Run agent (handles tool calling)
    state = agent(state)
    
    # Route and execute tools (Part 3 logic)
    route = route_tools(state)
    if route != "end" and not state["interrupt"]:
        state = execute_tools(state, route)
    
    # Cap history to last 10
    return state["messages"][-10:]