# excursions.py - Excursion tools with SQLite
import sqlite3
from dotenv import load_dotenv
load_dotenv()
db = 'data/travel2.sqlite'

def search_excursions(location):
    """Search excursions."""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    query = "SELECT * FROM excursions WHERE 1=1"
    params = []
    if location:
        query += " AND location = ?"
        params.append(location)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    conn.close()
    return results

def book_excursion(excursion_id, passenger_id):
    """Book excursion."""
    if not passenger_id:
        raise ValueError("No passenger ID.")
    # Mock book
    return "Excursion booked successfully."