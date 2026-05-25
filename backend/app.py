from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from routes.analyze import router as analyze_router
import os

app = FastAPI(
    title="FixForge API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(analyze_router)

@app.get("/")
async def root():
    # Return index.html from the frontend folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(os.path.dirname(current_dir), "frontend", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "project": "FixForge",
        "status": "running",
        "info": "frontend/index.html not found"
    }


    