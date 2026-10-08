from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from backend.models.context import CampaignContext
from backend.models.asset import Asset

class ContentStrategyPlan(BaseModel):
    summary: str = Field(..., description="High level campaign summary")
    pillars: List[str] = Field(default_factory=list, description="Key messaging pillars")
    platform_roles: Dict[str, str] = Field(default_factory=dict, description="Platform purpose breakdown")
    timeline_milestones: List[str] = Field(default_factory=list, description="Rollout sequence")
    multilingual_strategy: str = Field("", description="How regional and native languages are deployed")

class Campaign(BaseModel):
    id: str = Field(..., description="Campaign unique ID")
    title: str = Field(..., description="Campaign title")
    status: str = Field("IN_REVIEW", description="DRAFT, GENERATING, IN_REVIEW, CAMPAIGN_READY, PUBLISHED")
    context: CampaignContext = Field(..., description="Extracted & customized context engine configuration")
    strategy_plan: Optional[ContentStrategyPlan] = Field(None, description="AI strategic rollout plan")
    assets: List[Asset] = Field(default_factory=list, description="Coordinated multimodal assets")
    created_at: str = Field(..., description="ISO creation timestamp")
    updated_at: str = Field(..., description="ISO updated timestamp")
    notes: Optional[str] = Field(None)

class GenerationRequest(BaseModel):
    prompt: str = Field(..., description="Natural language prompt from the Super Prompt Bar")
    campaign_id: Optional[str] = Field(None, description="Optional existing campaign ID to augment")
    language: Optional[str] = Field("English", description="Target primary language")
    region: Optional[str] = Field("India / Global", description="Target region")
    platforms: Optional[List[str]] = Field(None, description="Target platforms")
    content_types: Optional[List[str]] = Field(None, description="Media types to generate")
    tone: Optional[List[str]] = Field(None, description="Tone attributes")
    brand_id: Optional[str] = Field(None, description="Active brand ID")

class GenerationJobResponse(BaseModel):
    job_id: str
    campaign_id: str
    status: str  # QUEUED, PROCESSING, COMPLETED, FAILED
    step_index: int
    current_step: str
    total_steps: int
    steps: List[Dict[str, Any]]
    campaign: Optional[Campaign] = None
    error: Optional[str] = None
