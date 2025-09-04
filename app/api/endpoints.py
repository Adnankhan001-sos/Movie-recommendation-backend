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
    return {"status": "healthy", "message": "Movie Recommendation API is running"}

@router.get("/genres", response_model=GenreResponse)
async def get_genres():
    """Get all available movie genres"""
    try:
        genres = movie_service.get_all_genres()
        print(f"📊 Found {len(genres)} genres: {genres}")
        return GenreResponse(genres=genres)
    except Exception as e:
        print(f"❌ Error getting genres: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting genres: {str(e)}")

@router.get("/movies/recommendations", response_model=RecommendationResponse)
async def get_movie_recommendations(
    genre: str = Query(..., description="Movie genre to filter by"),
    count: int = Query(6, ge=1, le=20, description="Number of recommendations to return")
):
    """Get random movie recommendations by genre"""
    try:
        print(f"🎬 Getting {count} recommendations for genre: {genre}")
        
        # First check if genre exists
        available_genres = movie_service.get_all_genres()
        if genre not in available_genres:
            print(f"❌ Genre '{genre}' not found. Available: {available_genres}")
            raise HTTPException(
                status_code=400, 
                detail=f"Genre '{genre}' not found. Available genres: {', '.join(available_genres)}"
            )
        
        recommendations = recommendation_service.get_recommendations(genre, count)
        print(f"✅ Found {len(recommendations)} recommendations")
        
        if not recommendations:
            raise HTTPException(status_code=404, detail=f"No movies found for genre: {genre}")
        
        return RecommendationResponse(movies=recommendations, count=len(recommendations))
    
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"❌ Unexpected error getting recommendations: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error getting recommendations: {str(e)}")

@router.get("/movies/{movie_id}", response_model=Movie)
async def get_movie_details(movie_id: int):
    """Get detailed information about a specific movie"""
    try:
        print(f"🎥 Getting details for movie ID: {movie_id}")
        movie = movie_service.get_movie_details(movie_id)
        
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        return movie
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error getting movie details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting movie details: {str(e)}")

# Debug endpoint to check database contents
@router.get("/debug/movies")
async def debug_movies():
    """Debug endpoint to check what's in the database"""
    try:
        from app.services.database_service import DatabaseService
        db_service = DatabaseService()
        
        conn = db_service.get_connection()
        cursor = conn.cursor()
        
        # Count total movies
        cursor.execute("SELECT COUNT(*) FROM movies")
        total_count = cursor.fetchone()[0]
        
        # Count by genre
        cursor.execute("SELECT genre, COUNT(*) FROM movies GROUP BY genre")
        genre_counts = dict(cursor.fetchall())
        
        # Get sample movies
        cursor.execute("SELECT id, title, genre FROM movies LIMIT 10")
        sample_movies = [{"id": row[0], "title": row[1], "genre": row[2]} for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            "total_movies": total_count,
            "movies_by_genre": genre_counts,
            "sample_movies": sample_movies
        }
    except Exception as e:
        return {"error": str(e)}
