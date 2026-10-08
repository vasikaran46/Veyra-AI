from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from backend.config import settings

router = APIRouter(prefix="/api/system", tags=["system"])

class SettingsUpdate(BaseModel):
    demo_mode: Optional[bool] = None
    text_model: Optional[str] = None
    image_model: Optional[str] = None

@router.get("/config")
async def get_system_config():
    return {
        "project_name": settings.PROJECT_NAME,
        "tagline": settings.TAGLINE,
        "version": settings.VERSION,
        "demo_mode": settings.is_demo_mode,
        "has_groq": bool(settings.GROQ_API_KEY.strip()),
        "has_replicate": bool(settings.REPLICATE_API_TOKEN.strip()),
        "has_supabase": settings.has_supabase,
        "text_model": settings.TEXT_MODEL,
        "image_model": settings.IMAGE_MODEL,
        "video_model": settings.VIDEO_MODEL,
        "audio_model": settings.AUDIO_MODEL,
        "supported_languages": [
            {"code": "en", "name": "English", "native": "English"},
            {"code": "ta", "name": "Tamil", "native": "தமிழ்"},
            {"code": "hi", "name": "Hindi", "native": "हिंदी"},
            {"code": "te", "name": "Telugu", "native": "తెలుగు"},
            {"code": "ml", "name": "Malayalam", "native": "മലയാളം"},
            {"code": "kn", "name": "Kannada", "native": "ಕನ್ನಡ"},
            {"code": "bn", "name": "Bengali", "native": "বাংলা"}
        ]
    }

@router.post("/config")
async def update_system_config(req: SettingsUpdate):
    if req.demo_mode is not None:
        settings.FORCE_DEMO_MODE = req.demo_mode
    if req.text_model is not None:
        settings.TEXT_MODEL = req.text_model
    if req.image_model is not None:
        settings.IMAGE_MODEL = req.image_model
    return {"status": "updated", "demo_mode": settings.is_demo_mode}
