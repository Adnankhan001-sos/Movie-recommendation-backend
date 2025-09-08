from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router

app = FastAPI(
    title="Movie Recommendation API", 
    version="2.0.0",
    description="Real movie recommendations powered by The Movie Database (TMDB)"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for deployed frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "Movie Recommendation API v2.0 with TMDB integration!", 
        "status": "healthy",
        "version": "2.0.0",
        "powered_by": "The Movie Database (TMDB)"
    }
