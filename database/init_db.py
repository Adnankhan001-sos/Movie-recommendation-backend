import os
from app.services.database_service import DatabaseService
from database.seed_data import SEED_MOVIES

def initialize_database():
    """Initialize the database with tables and seed data"""
    db_service = DatabaseService()
    
    # Create tables
    db_service.create_tables()
    
    # Check if data already exists
    conn = db_service.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM movies")
    count = cursor.fetchone()[0]
    conn.close()
    
    # Insert seed data if table is empty
    if count == 0:
        print("Inserting seed data...")
        db_service.insert_movies(SEED_MOVIES)
        print(f"Inserted {len(SEED_MOVIES)} movies into database")
    else:
        print(f"Database already contains {count} movies")

if __name__ == "__main__":
    initialize_database()
