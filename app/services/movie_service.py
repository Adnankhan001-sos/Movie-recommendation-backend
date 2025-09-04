from typing import List, Optional
from app.services.database_service import DatabaseService
from app.models import Movie

class MovieService:
    def __init__(self):
        self.db_service = DatabaseService()
    
    def get_all_genres(self) -> List[str]:
        return self.db_service.get_all_genres()
    
    def get_movie_details(self, movie_id: int) -> Optional[Movie]:
        return self.db_service.get_movie_by_id(movie_id)
