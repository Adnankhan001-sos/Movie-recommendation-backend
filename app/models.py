from pydantic import BaseModel, Field
from typing import List, Optional

class Movie(BaseModel):
    id: int
    title: str
    year: int
    genre: str
    description: str
    rating: float
    runtime: int
    poster_url: Optional[str] = None
    
    class Config:
        from_attributes = True
        # Allow arbitrary types and extra fields
        extra = "ignore"

class MovieSummary(BaseModel):
    id: int
    title: str
    year: int
    genre: str
    rating: float
    poster_url: Optional[str] = None
    
    class Config:
        from_attributes = True
        extra = "ignore"

class GenreResponse(BaseModel):
    genres: List[str]
    
    class Config:
        extra = "ignore"

class RecommendationResponse(BaseModel):
    movies: List[MovieSummary]
    count: int
    
    class Config:
        extra = "ignore"
