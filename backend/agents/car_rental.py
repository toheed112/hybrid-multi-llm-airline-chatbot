# car_rental.py - Specialized car rental agent
from .primary_assistant import agent

def car_rental_assistant(state: dict) -> dict:
    """Car rental expert assistant."""
    # Use primary agent with car-specific prompt
    state = agent(state)
    return state