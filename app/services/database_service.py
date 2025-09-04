import sqlite3
import os
from typing import List, Optional
from app.models import Movie

class DatabaseService:
    def __init__(self, db_path: str = "database/movies.db"):
        self.db_path = db_path
        # Ensure database directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                year INTEGER NOT NULL,
                genre TEXT NOT NULL,
                description TEXT NOT NULL,
                rating REAL NOT NULL,
                runtime INTEGER NOT NULL,
                poster_url TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def insert_movies(self, movies: List[dict]):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.executemany("""
            INSERT INTO movies (title, year, genre, description, rating, runtime, poster_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [(
            movie["title"], movie["year"], movie["genre"], 
            movie["description"], movie["rating"], movie["runtime"], 
            movie.get("poster_url", "/placeholder.jpg")
        ) for movie in movies])
        
        conn.commit()
        conn.close()
    
    def get_all_genres(self) -> List[str]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT genre FROM movies ORDER BY genre")
        genres = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return genres
    
    def get_movies_by_genre(self, genre: str, limit: int = 10) -> List[Movie]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, year, genre, description, rating, runtime, poster_url
            FROM movies 
            WHERE genre = ? 
            ORDER BY RANDOM() 
            LIMIT ?
        """, (genre, limit))
        
        movies = []
        for row in cursor.fetchall():
            movies.append(Movie(
                id=row[0], title=row[1], year=row[2], genre=row[3],
                description=row[4], rating=row[5], runtime=row[6], poster_url=row[7]
            ))
        
        conn.close()
        return movies
    
    def get_movie_by_id(self, movie_id: int) -> Optional[Movie]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, year, genre, description, rating, runtime, poster_url
            FROM movies 
            WHERE id = ?
        """, (movie_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Movie(
                id=row[0], title=row[1], year=row[2], genre=row[3],
                description=row[4], rating=row[5], runtime=row[6], poster_url=row[7]
            )
        return None
