import datetime
from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Query
from backend.models.asset import Asset, AssetStatus
from backend.services.orchestrator import CAMPAIGNS_STORE
from backend.services.model_router import model_router

router = APIRouter(prefix="/api/assets", tags=["assets"])

class AssetUpdateRequest(BaseModel):
    content: Optional[str] = None
    hook: Optional[str] = None
    call_to_action: Optional[str] = None
    prompt: Optional[str] = None
    aspect_ratio: Optional[str] = None
    status: Optional[AssetStatus] = None
    edit_notes: Optional[str] = None

class AssetRegenerateRequest(BaseModel):
    feedback: Optional[str] = None
    target_tone: Optional[str] = None

class AssetTranslateRequest(BaseModel):
    target_language: str

def find_asset(asset_id: str):
    for camp in CAMPAIGNS_STORE.values():
        for ast in camp.assets:
            if ast.id == asset_id:
                return camp, ast
    return None, None

@router.get("", response_model=List[Asset])
async def list_assets(
    campaign_id: Optional[str] = None,
    platform: Optional[str] = None,
    asset_type: Optional[str] = None,
    status: Optional[str] = None,
    language: Optional[str] = None,
    search: Optional[str] = None
):
    """List assets with flexible Content Library filtering."""
    results: List[Asset] = []
    seen = set()

    for camp in CAMPAIGNS_STORE.values():
        if campaign_id and camp.id != campaign_id:
            continue
        for ast in camp.assets:
            if ast.id in seen:
                continue
            seen.add(ast.id)

            if platform and platform.lower() not in ast.platform.lower():
                continue
            if asset_type and asset_type.upper() != ast.type.value:
                continue
            if status and status.upper() != ast.status.value:
                continue
            if language and language.lower() not in ast.language.lower():
                continue
            if search:
                s_lower = search.lower()
                text_match = (
                    s_lower in ast.title.lower() or
                    (ast.content and s_lower in ast.content.lower()) or
                    (ast.prompt and s_lower in ast.prompt.lower()) or
                    s_lower in ast.platform.lower()
                )
                if not text_match:
                    continue

            results.append(ast)

    return sorted(results, key=lambda x: x.created_at or "", reverse=True)

@router.get("/{asset_id}", response_model=Asset)
async def get_asset(asset_id: str):
    _, ast = find_asset(asset_id)
    if not ast:
        raise HTTPException(status_code=404, detail="Asset not found")
    return ast

@router.patch("/{asset_id}", response_model=Asset)
async def update_asset(asset_id: str, req: AssetUpdateRequest):
    camp, ast = find_asset(asset_id)
    if not ast:
        raise HTTPException(status_code=404, detail="Asset not found")

    if req.content is not None:
        ast.content = req.content
        ast.character_count = len(req.content)
    if req.hook is not None:
        ast.hook = req.hook
    if req.call_to_action is not None:
        ast.call_to_action = req.call_to_action
    if req.prompt is not None:
        ast.prompt = req.prompt
    if req.aspect_ratio is not None:
        ast.aspect_ratio = req.aspect_ratio
    if req.status is not None:
        ast.status = req.status
    if req.edit_notes is not None:
        ast.edit_notes = req.edit_notes

    ast.status = AssetStatus.EDITED
    ast.version += 1
    ast.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if camp:
        camp.updated_at = ast.updated_at
    return ast

@router.post("/{asset_id}/approve", response_model=Asset)
async def approve_asset(asset_id: str):
    camp, ast = find_asset(asset_id)
    if not ast:
        raise HTTPException(status_code=404, detail="Asset not found")

    ast.status = AssetStatus.APPROVED
    ast.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Check if all assets in campaign are now approved
    if camp:
        if all(a.status == AssetStatus.APPROVED for a in camp.assets):
            camp.status = "CAMPAIGN_READY"
        camp.updated_at = ast.updated_at

    return ast

@router.post("/{asset_id}/regenerate", response_model=Asset)
async def regenerate_asset(asset_id: str, req: AssetRegenerateRequest):
    camp, ast = find_asset(asset_id)
    if not ast:
        raise HTTPException(status_code=404, detail="Asset not found")

    context = camp.context if camp else None
    
    if ast.type.value == "TEXT" and context:
        res = await model_router.generate_text(
            platform=ast.platform,
            context=context,
            target_language=ast.language,
            refinement_instructions=req.feedback
        )
        ast.content = res.get("content", ast.content)
        ast.hook = res.get("hook", ast.hook)
        ast.call_to_action = res.get("call_to_action", ast.call_to_action)
        ast.hashtags = res.get("hashtags", ast.hashtags)
        ast.character_count = len(ast.content or "")
    elif ast.type.value == "IMAGE" and context:
        new_prompt = f"{ast.prompt or 'High-end promotional image'}. Refinement: {req.feedback or 'More vibrant focus'}"
        res = await model_router.generate_image(
            prompt=new_prompt,
            aspect_ratio=ast.aspect_ratio or "4:5",
            context=context,
            overlay_language=ast.language
        )
        ast.prompt = new_prompt
        ast.media_url = res.get("media_url", ast.media_url)
    elif ast.type.value == "VIDEO" and context:
        res = await model_router.generate_video(
            prompt=ast.prompt or f"Promo video for {context.subject}",
            context=context,
            language=ast.language
        )
        ast.video_storyboard = res.get("storyboard", ast.video_storyboard)
        ast.subtitles = res.get("subtitles", ast.subtitles)
    elif ast.type.value == "AUDIO" and context:
        res = await model_router.generate_audio(
            context=context,
            language=ast.language
        )
        ast.audio_transcript = res.get("audio_transcript", ast.audio_transcript)
        ast.waveform_data = res.get("waveform_data", ast.waveform_data)

    ast.status = AssetStatus.READY_FOR_REVIEW
    ast.version += 1
    ast.edit_notes = f"Regenerated with note: {req.feedback}" if req.feedback else "Regenerated"
    ast.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return ast

@router.post("/{asset_id}/translate", response_model=Asset)
async def translate_asset(asset_id: str, req: AssetTranslateRequest):
    camp, ast = find_asset(asset_id)
    if not ast:
        raise HTTPException(status_code=404, detail="Asset not found")

    target_lang = req.target_language
    if ast.type.value == "TEXT" and ast.content:
        res = await model_router.translate(
            source_text=ast.content,
            target_language=target_lang,
            platform=ast.platform
        )
        ast.content = res.get("translated_text", ast.content)
        ast.hook = res.get("hook", ast.hook)
        ast.call_to_action = res.get("call_to_action", ast.call_to_action)
        ast.language = target_lang
        ast.title = f"{ast.title.split('(')[0].strip()} ({target_lang})"
        ast.character_count = len(ast.content or "")
    elif ast.type.value == "IMAGE":
        ast.language = f"{target_lang} & English"
        ast.overlay_language = target_lang
        if camp:
            if "tamil" in target_lang.lower():
                ast.overlay_text = f"{camp.context.subject} — உங்கள் எதிர்காலத்தை இன்றே கட்டமைப்போம்"
            elif "hindi" in target_lang.lower():
                ast.overlay_text = f"{camp.context.subject} — नवाचार की नई उड़ान"
            else:
                ast.overlay_text = f"{camp.context.subject} — Build the Intelligent Future"
    elif ast.type.value == "VIDEO" and camp:
        res = await model_router.generate_video(
            prompt=ast.prompt or "Video promo",
            context=camp.context,
            language=target_lang
        )
        ast.language = f"{target_lang} (Voice) + Subtitles"
        ast.subtitles = res.get("subtitles", ast.subtitles)
    elif ast.type.value == "AUDIO" and camp:
        res = await model_router.generate_audio(
            context=camp.context,
            language=target_lang
        )
        ast.language = target_lang
        ast.audio_transcript = res.get("audio_transcript", ast.audio_transcript)
        ast.voice_name = res.get("voice_name", ast.voice_name)

    ast.status = AssetStatus.READY_FOR_REVIEW
    ast.version += 1
    ast.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return ast
