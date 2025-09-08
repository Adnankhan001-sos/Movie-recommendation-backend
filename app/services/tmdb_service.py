import requests
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class TMDBService:
    def __init__(self):
        self.api_key = os.getenv('TMDB_API_KEY')
        self.base_url = os.getenv('TMDB_BASE_URL', 'https://api.themoviedb.org/3')
        self.image_base_url = "https://image.tmdb.org/t/p/w500"
        
        if not self.api_key:
            raise ValueError("TMDB_API_KEY not found in environment variables")
    
    def get_genre_list(self) -> Dict:
        """Get TMDB genre list"""
        url = f"{self.base_url}/genre/movie/list"
        params = {'api_key': self.api_key}
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def discover_movies_by_genre(self, genre_id: int, page: int = 1) -> Dict:
        """Discover movies by genre"""
        url = f"{self.base_url}/discover/movie"
        params = {
            'api_key': self.api_key,
            'with_genres': genre_id,
            'page': page,
            'sort_by': 'popularity.desc',
            'include_adult': False,
            'language': 'en-US',
            'vote_count.gte': 100  # Only movies with decent number of votes
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_movie_details(self, tmdb_id: int) -> Dict:
        """Get detailed movie information"""
        url = f"{self.base_url}/movie/{tmdb_id}"
        params = {
            'api_key': self.api_key,
            'language': 'en-US'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def format_movie_data(self, tmdb_movie: Dict, genre_name: str) -> Dict:
        """Format TMDB movie data to our model format"""
        return {
            'tmdb_id': tmdb_movie['id'],
            'title': tmdb_movie['title'],
            'year': int(tmdb_movie['release_date'][:4]) if tmdb_movie.get('release_date') else 2024,
            'genre': genre_name,
            'description': tmdb_movie.get('overview', 'No description available.'),
            'rating': round(tmdb_movie.get('vote_average', 0), 1),
            'poster_url': f"{self.image_base_url}{tmdb_movie['poster_path']}" if tmdb_movie.get('poster_path') else None,
            'runtime': tmdb_movie.get('runtime')
        }

# Global TMDB service instance
tmdb_service = TMDBService()
