from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.services.movie_service import MovieService
from app.services.recommendation_service import RecommendationService
from app.models import GenreResponse, RecommendationResponse, Movie

router = APIRouter()

# Initialize services
movie_service = MovieService()
recommendation_service = RecommendationService()

@router.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Movie Recommendation API v2.0 with TMDB", "version": "2.0"}

@router.get("/genres", response_model=GenreResponse)
async def get_genres():
    """Get all available movie genres"""
    try:
        genres = movie_service.get_all_genres()
        return GenreResponse(genres=genres)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting genres: {str(e)}")

@router.get("/movies/recommendations", response_model=RecommendationResponse)
async def get_movie_recommendations(
    genre: str = Query(..., description="Movie genre to filter by"),
    count: int = Query(6, ge=1, le=20, description="Number of recommendations to return")
):
    """Get random movie recommendations by genre from TMDB"""
    try:
        available_genres = movie_service.get_all_genres()
        if genre not in available_genres:
            raise HTTPException(
                status_code=400, 
                detail=f"Genre '{genre}' not found. Available genres: {', '.join(available_genres)}"
            )
        
        recommendations = recommendation_service.get_recommendations(genre, count)
        
        if not recommendations:
            raise HTTPException(status_code=404, detail=f"No movies found for genre: {genre}")
        
        return RecommendationResponse(movies=recommendations, count=len(recommendations))
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recommendations: {str(e)}")

@router.get("/movies/{movie_id}", response_model=Movie)
async def get_movie_details(movie_id: int):
    """Get detailed information about a specific movie from TMDB"""
    try:
        movie = movie_service.get_movie_details(movie_id)
        
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        return movie
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting movie details: {str(e)}")
