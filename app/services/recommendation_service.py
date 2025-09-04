from typing import List
from app.services.database_service import DatabaseService
from app.models import Movie, MovieSummary

class RecommendationService:
    def __init__(self):
        self.db_service = DatabaseService()
    
    def get_recommendations(self, genre: str, count: int = 6) -> List[MovieSummary]:
        movies = self.db_service.get_movies_by_genre(genre, count)
        
        # Convert to MovieSummary for lighter response
        return [
            MovieSummary(
                id=movie.id,
                title=movie.title,
                year=movie.year,
                genre=movie.genre,
                rating=movie.rating,
                poster_url=movie.poster_url
            ) for movie in movies
        ]
