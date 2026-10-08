import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.config import settings
from backend.api.campaigns import router as campaigns_router
from backend.api.generation import router as generation_router
from backend.api.assets import router as assets_router
from backend.api.brand import router as brand_router
from backend.api.history import router as history_router
from backend.api.settings_api import router as system_router

ROOT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT_DIR / "frontend"
ASSETS_DIR = ROOT_DIR / "assets"

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=f"{settings.TAGLINE} — Context-Aware Multilingual Multimodal AI Content Creation & Refinement Platform",
    version=settings.VERSION
)

# Enable CORS for frontend flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(campaigns_router)
app.include_router(generation_router)
app.include_router(assets_router)
app.include_router(brand_router)
app.include_router(history_router)
app.include_router(system_router)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "tagline": settings.TAGLINE,
        "demo_mode": settings.is_demo_mode
    }

# Mount assets directory for generated and static media
if ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")

# Mount locales directory for i18n
LOCALES_DIR = FRONTEND_DIR / "locales"
if LOCALES_DIR.exists():
    app.mount("/locales", StaticFiles(directory=str(LOCALES_DIR)), name="locales")

# Mount frontend static directory if exists
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/")
async def serve_index():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "Veyra AI backend active. Frontend index.html being built."}

# Catch-all for SPA views or direct static asset requests
@app.get("/{file_name}")
async def serve_frontend_file(file_name: str):
    file_path = FRONTEND_DIR / file_name
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"error": "Not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
