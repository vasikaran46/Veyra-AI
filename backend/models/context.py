from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class CampaignContext(BaseModel):
    subject: str = Field(..., description="Main topic or campaign subject")
    objective: str = Field("Increase engagement & registrations", description="Goal of the campaign")
    audience: str = Field("Engineering students and tech enthusiasts", description="Target audience segment")
    platforms: List[str] = Field(default_factory=lambda: ["Instagram", "LinkedIn", "YouTube Shorts"])
    tone: List[str] = Field(default_factory=lambda: ["Energetic", "Professional", "Inspiring"])
    language: str = Field("English", description="Primary campaign language")
    region: str = Field("India / Global", description="Target region or market")
    brand: Dict[str, Any] = Field(default_factory=dict, description="Brand memory guidelines")
    content_types: List[str] = Field(default_factory=lambda: ["Text", "Image", "Video", "Audio"])
    extra_instructions: Optional[str] = Field(None, description="Additional custom instructions")
