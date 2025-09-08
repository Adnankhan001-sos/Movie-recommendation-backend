"""
FastAPI server startup script with TMDB integration
"""
import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🎬 Starting Movie Recommendation API Server v2.0...")
    print("📍 Server: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🎭 Powered by TMDB - Real movies, real posters!")
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
