# car_rentals.py - Car rental search/book tools with SQLite
import sqlite3
from dotenv import load_dotenv
load_dotenv()
db = 'data/travel2.sqlite'

def search_cars(location, dates=None, limit=20):
    """Search cars."""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    query = "SELECT * FROM cars WHERE 1=1"
    params = []
    if location:
        query += " AND location = ?"
        params.append(location)
    query += " LIMIT ?"
    params.append(limit)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    conn.close()
    if not results:
        return "No cars found for your location. Try broader search."
    return results

def book_car(car_id, passenger_id):
    """Book car."""
    if not passenger_id:
        raise ValueError("No passenger ID.")
    # Mock book (add DB update in prod)
    return "Car booked successfully."