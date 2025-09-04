"""
FastAPI server startup script
Run this to start the movie recommendation API server
"""
import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🎬 Starting Movie Recommendation API Server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔧 Interactive API: http://localhost:8000/redoc")
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
