# hotels.py - Hotel tools with SQLite
import sqlite3
from dotenv import load_dotenv
load_dotenv()
db = 'data/travel2.sqlite'

def search_hotels(location, checkin=None, checkout=None):
    """Search hotels."""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    query = "SELECT * FROM hotels WHERE 1=1"
    params = []
    if location:
        query += " AND location = ?"
        params.append(location)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    conn.close()
    if not results:
        return "No hotels found."
    return results

def book_hotel(hotel_id, passenger_id):
    """Book hotel."""
    if not passenger_id:
        raise ValueError("No passenger ID.")
    return "Hotel booked successfully."