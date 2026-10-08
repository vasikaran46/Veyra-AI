import uuid
import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from backend.models.campaign import Campaign
from backend.models.context import CampaignContext
from backend.models.asset import AssetStatus
from backend.services.orchestrator import CAMPAIGNS_STORE

router = APIRouter(prefix="/api/campaigns", tags=["campaigns"])

@router.get("", response_model=List[Campaign])
async def list_campaigns():
    """List all campaigns in reverse chronological order."""
    unique_campaigns = {c.id: c for c in CAMPAIGNS_STORE.values()}
    return sorted(unique_campaigns.values(), key=lambda x: x.created_at, reverse=True)

@router.get("/{campaign_id}", response_model=Campaign)
async def get_campaign(campaign_id: str):
    """Retrieve a single campaign by ID or 'default'."""
    camp = CAMPAIGNS_STORE.get(campaign_id)
    if not camp:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return camp

@router.post("", response_model=Campaign)
async def create_campaign(context: CampaignContext, title: Optional[str] = None):
    """Create a new campaign container with context."""
    camp_id = f"camp_{uuid.uuid4().hex[:8]}"
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    camp = Campaign(
        id=camp_id,
        title=title or context.subject,
        status="DRAFT",
        context=context,
        assets=[],
        created_at=now,
        updated_at=now
    )
    CAMPAIGNS_STORE[camp_id] = camp
    CAMPAIGNS_STORE["default"] = camp
    return camp

@router.post("/{campaign_id}/approve-all", response_model=Campaign)
async def approve_all_assets(campaign_id: str):
    """Approve all assets in the campaign and mark the campaign CAMPAIGN_READY."""
    camp = CAMPAIGNS_STORE.get(campaign_id)
    if not camp:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    for asset in camp.assets:
        asset.status = AssetStatus.APPROVED
    
    camp.status = "CAMPAIGN_READY"
    camp.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return camp
