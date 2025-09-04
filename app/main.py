from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create the app instance
app = FastAPI(title="Movie Recommendation API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic root route
@app.get("/")
async def root():
    return {"message": "Movie Recommendation API is running!", "status": "healthy"}

# Import and include routes immediately (not in startup event)
try:
    from app.api.endpoints import router
    app.include_router(router, prefix="/api")
    print("✅ API routes included successfully")
except Exception as e:
    print(f"❌ Error including routes: {e}")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    try:
        from database.init_db import initialize_database
        initialize_database()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
