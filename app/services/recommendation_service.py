import random
from typing import List
from app.services.tmdb_service import tmdb_service
from app.models import MovieSummary

class RecommendationService:
    def __init__(self):
        # TMDB Genre IDs mapping
        self.genre_mapping = {
            'Action': 28,
            'Adventure': 12,
            'Animation': 16,
            'Comedy': 35,
            'Crime': 80,
            'Documentary': 99,
            'Drama': 18,
            'Family': 10751,
            'Fantasy': 14,
            'History': 36,
            'Horror': 27,
            'Music': 10402,
            'Mystery': 9648,
            'Romance': 10749,
            'Sci-Fi': 878,
            'Thriller': 53,
            'War': 10752,
            'Western': 37
        }
    
    def get_recommendations(self, genre: str, count: int = 6) -> List[MovieSummary]:
        """Get movie recommendations from TMDB API"""
        try:
            genre_id = self.genre_mapping.get(genre)
            if not genre_id:
                return []
            
            # Get movies from TMDB (fetch from random pages for variety)
            page = random.randint(1, 5)  # Random page for variety
            tmdb_response = tmdb_service.discover_movies_by_genre(genre_id, page)
            
            movies = tmdb_response.get('results', [])
            
            # Filter out movies without posters for better UX
            movies_with_posters = [m for m in movies if m.get('poster_path')]
            
            # Use all movies if no posters available
            if not movies_with_posters:
                movies_with_posters = movies
            
            # Randomly select the requested count
            if len(movies_with_posters) > count:
                movies_with_posters = random.sample(movies_with_posters, count)
            
            # Format movies to our model
            recommendations = []
            for movie in movies_with_posters:
                formatted_movie = tmdb_service.format_movie_data(movie, genre)
                recommendations.append(MovieSummary(
                    id=formatted_movie['tmdb_id'],
                    tmdb_id=formatted_movie['tmdb_id'],
                    title=formatted_movie['title'],
                    year=formatted_movie['year'],
                    genre=formatted_movie['genre'],
                    rating=formatted_movie['rating'],
                    poster_url=formatted_movie['poster_url']
                ))
            
            return recommendations
            
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return []
