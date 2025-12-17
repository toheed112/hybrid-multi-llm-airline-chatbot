# Tools init - Exports all tool functions and globals for graph
from .policy import lookup_policy
from .flights import search_flights, update_ticket_to_new_flight
from .car_rentals import search_cars, book_car
from .hotels import search_hotels, book_hotel
from .excursions import search_excursions, book_excursion
from .utilities import fetch_user_info, search_web

# Global constants for graph (used in workflow.py)
TOOLS_DESC = "\n".join([
    f"- lookup_policy(query): Lookup company policies via embeddings.",
    f"- search_flights(departure_airport, limit): Search flights.",
    f"- search_web(query): Web search via Tavily for live info.",
    f"- book_hotel(hotel_id, passenger_id): Book hotel.",
    f"- search_cars(location, dates): Search cars.",
    f"- search_hotels(location, checkin, checkout): Search hotels.",
    f"- search_excursions(location): Search excursions.",
    f"- update_ticket_to_new_flight(ticket_no, new_flight_id, passenger_id): Update ticket.",
    f"- book_car(car_id, passenger_id): Book car.",
    f"- book_excursion(excursion_id, passenger_id): Book excursion.",
    f"- fetch_user_info(passenger_id): Fetch user bookings.",
])

SENSITIVE_TOOLS = {"book_hotel", "update_ticket_to_new_flight", "book_car", "book_excursion"}

__all__ = [
    'lookup_policy', 'search_flights', 'update_ticket_to_new_flight',
    'search_cars', 'book_car', 'search_hotels', 'book_hotel', 'search_excursions', 'book_excursion',
    'fetch_user_info', 'search_web', 'TOOLS_DESC', 'SENSITIVE_TOOLS'
]