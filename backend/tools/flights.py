# flights.py - Flight search/update tools with SQLite
import sqlite3
from dotenv import load_dotenv
load_dotenv()
db = 'data/travel2.sqlite'

def search_flights(departure_airport=None, arrival_airport=None, limit=20):
    """Search flights."""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    query = "SELECT * FROM flights WHERE 1=1"
    params = []
    if departure_airport:
        query += " AND departure_airport = ?"
        params.append(departure_airport)
    if arrival_airport:
        query += " AND arrival_airport = ?"
        params.append(arrival_airport)
    query += " LIMIT ?"
    params.append(limit)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    conn.close()
    if not results:
        return "No flights found for your criteria. Try broader search."
    return results

def update_ticket_to_new_flight(ticket_no, new_flight_id, passenger_id):
    """Update ticket (with passenger check)."""
    if not passenger_id:
        raise ValueError("No passenger ID.")
    # Mock update (add DB update in prod)
    return "Ticket updated successfully."