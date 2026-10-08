from typing import Dict, Any, Optional
from backend.services.text_service import text_service
from backend.services.image_service import image_service
from backend.services.video_service import video_service
from backend.services.audio_service import audio_service
from backend.services.translation_service import translation_service
from backend.models.context import CampaignContext

class ModelRouter:
    """
    Central provider abstraction routing media generation tasks to appropriate specialized services.
    Decouples provider-specific APIs from application and orchestration logic.
    """
    async def generate_text(
        self,
        platform: str,
        context: CampaignContext,
        target_language: str = "English",
        refinement_instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        return await text_service.generate_platform_copy(
            platform=platform,
            context=context,
            target_language=target_language,
            refinement_instructions=refinement_instructions
        )

    async def generate_image(
        self,
        prompt: str,
        aspect_ratio: str = "4:5",
        context: Optional[CampaignContext] = None,
        overlay_text: Optional[str] = None,
        overlay_language: Optional[str] = None
    ) -> Dict[str, Any]:
        return await image_service.generate_campaign_image(
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            context=context,
            overlay_text=overlay_text,
            overlay_language=overlay_language
        )

    async def generate_video(
        self,
        prompt: str,
        context: Optional[CampaignContext] = None,
        language: str = "Tamil"
    ) -> Dict[str, Any]:
        return await video_service.generate_campaign_video(
            prompt=prompt,
            context=context,
            language=language
        )

    async def generate_audio(
        self,
        context: Optional[CampaignContext] = None,
        language: str = "Tamil",
        voice_persona: Optional[str] = None
    ) -> Dict[str, Any]:
        return await audio_service.generate_campaign_audio(
            context=context,
            language=language,
            voice_persona=voice_persona
        )

    async def translate(
        self,
        source_text: str,
        target_language: str,
        platform: str = "General",
        tone: Optional[str] = "Professional",
        brand_voice: Optional[str] = None
    ) -> Dict[str, Any]:
        return await translation_service.translate_content(
            source_text=source_text,
            target_language=target_language,
            platform=platform,
            tone=tone,
            brand_voice=brand_voice
        )

model_router = ModelRouter()
