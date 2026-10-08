from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class AssetType(str, Enum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"

class AssetStatus(str, Enum):
    GENERATING = "GENERATING"
    READY_FOR_REVIEW = "READY_FOR_REVIEW"
    EDITED = "EDITED"
    APPROVED = "APPROVED"
    NEEDS_REGENERATION = "NEEDS_REGENERATION"

class Asset(BaseModel):
    id: str = Field(..., description="Unique asset identifier")
    campaign_id: str = Field(..., description="Parent campaign ID")
    type: AssetType = Field(..., description="Media type: TEXT, IMAGE, VIDEO, AUDIO")
    title: str = Field(..., description="Short asset title or headline")
    platform: str = Field(..., description="Target platform, e.g., Instagram, LinkedIn, YouTube Shorts")
    language: str = Field("English", description="Asset specific language")
    status: AssetStatus = Field(AssetStatus.READY_FOR_REVIEW, description="Review lifecycle status")
    
    # Text asset attributes
    content: Optional[str] = Field(None, description="Primary textual content or copy")
    character_count: Optional[int] = Field(None, description="Total characters")
    hashtags: List[str] = Field(default_factory=list, description="Platform relevant tags")
    hook: Optional[str] = Field(None, description="Initial hook sentence")
    call_to_action: Optional[str] = Field(None, description="CTA message")
    
    # Media asset attributes (Image / Video)
    media_url: Optional[str] = Field(None, description="URL or data URI for the generated media")
    aspect_ratio: Optional[str] = Field(None, description="e.g. 4:5, 1:1, 9:16, 16:9")
    prompt: Optional[str] = Field(None, description="Prompt passed to generation model")
    model_name: Optional[str] = Field(None, description="Model used for generation")
    
    # Image localization overlay
    overlay_text: Optional[str] = Field(None, description="Localized text overlay rendered cleanly")
    overlay_language: Optional[str] = Field(None, description="Language of the text overlay")
    
    # Video asset attributes
    duration_seconds: Optional[int] = Field(None, description="Estimated or actual duration")
    subtitles: List[Dict[str, Any]] = Field(default_factory=list, description="Subtitles timeline and language")
    video_storyboard: List[str] = Field(default_factory=list, description="Visual storyboard cues")
    
    # Audio asset attributes
    voice_name: Optional[str] = Field(None, description="Name or identifier of the voice persona")
    audio_duration: Optional[float] = Field(None, description="Duration in seconds")
    waveform_data: List[float] = Field(default_factory=list, description="Waveform amplitude sample values")
    audio_transcript: Optional[str] = Field(None, description="Spoken transcript")
    
    # History and notes
    version: int = Field(1, description="Asset version number")
    edit_notes: Optional[str] = Field(None, description="Human review modification notes")
    created_at: Optional[str] = Field(None)
    updated_at: Optional[str] = Field(None)
