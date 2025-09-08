from typing import List, Optional
from app.services.tmdb_service import tmdb_service
from app.models import Movie

class MovieService:
    def __init__(self):
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
    
    def get_all_genres(self) -> List[str]:
        """Get all available movie genres"""
        return list(self.genre_mapping.keys())
    
    def get_movie_details(self, tmdb_id: int) -> Optional[Movie]:
        """Get detailed movie information from TMDB"""
        try:
            tmdb_movie = tmdb_service.get_movie_details(tmdb_id)
            
            # Get genre name from the movie data
            genre_names = [g['name'] for g in tmdb_movie.get('genres', [])]
            primary_genre = genre_names[0] if genre_names else 'Unknown'
            
            # Map to our simplified genre if possible
            mapped_genre = primary_genre
            for our_genre, tmdb_id_map in self.genre_mapping.items():
                if primary_genre.lower() in our_genre.lower() or our_genre.lower() in primary_genre.lower():
                    mapped_genre = our_genre
                    break
            
            formatted_movie = tmdb_service.format_movie_data(tmdb_movie, mapped_genre)
            formatted_movie['id'] = tmdb_movie['id']
            
            return Movie(**formatted_movie)
            
        except Exception as e:
            print(f"Error getting movie details: {e}")
            return None
