from pydantic import BaseModel
from typing import List, Optional

class Movie(BaseModel):
    id: int
    title: str
    year: int
    genre: str
    description: str
    rating: float
    runtime: Optional[int] = None
    poster_url: Optional[str] = None
    tmdb_id: int
    
    class Config:
        from_attributes = True

class MovieSummary(BaseModel):
    id: int
    title: str
    year: int
    genre: str
    rating: float
    poster_url: Optional[str] = None
    tmdb_id: int
    
    class Config:
        from_attributes = True

class GenreResponse(BaseModel):
    genres: List[str]

class RecommendationResponse(BaseModel):
    movies: List[MovieSummary]
    count: int
