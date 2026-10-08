import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file from project root
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

class Settings(BaseSettings):
    PROJECT_NAME: str = "Veyra AI"
    TAGLINE: str = "From Context to Creation"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Groq
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    TEXT_MODEL: str = os.getenv("TEXT_MODEL", "llama-3.3-70b-versatile")

    # Replicate
    REPLICATE_API_TOKEN: str = os.getenv("REPLICATE_API_TOKEN", "")
    IMAGE_MODEL: str = os.getenv("IMAGE_MODEL", "black-forest-labs/flux-schnell")
    VIDEO_MODEL: str = os.getenv("VIDEO_MODEL", "minimax/video-01")
    AUDIO_MODEL: str = os.getenv("AUDIO_MODEL", "elevenlabs/speech-synthesis")

    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

    # Fallback & Demo
    FORCE_DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() == "true"

    @property
    def is_demo_mode(self) -> bool:
        # If API keys are missing or FORCE_DEMO_MODE is true, run in Demo Mode
        if self.FORCE_DEMO_MODE:
            return True
        return not bool(self.GROQ_API_KEY.strip())

    @property
    def has_replicate(self) -> bool:
        return bool(self.REPLICATE_API_TOKEN.strip())

    @property
    def has_supabase(self) -> bool:
        return bool(self.SUPABASE_URL.strip() and self.SUPABASE_KEY.strip())

settings = Settings()
