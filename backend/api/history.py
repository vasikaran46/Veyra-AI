from typing import List, Dict, Any
from fastapi import APIRouter
from backend.services.orchestrator import CAMPAIGNS_STORE, JOBS_STORE

router = APIRouter(prefix="/api/history", tags=["history"])

@router.get("", response_model=List[Dict[str, Any]])
async def get_history():
    """Retrieve history of generations and campaigns."""
    history = []
    seen = set()

    # Add from active campaigns
    for cid, camp in CAMPAIGNS_STORE.items():
        if cid == "default" or cid in seen:
            continue
        seen.add(cid)
        history.append({
            "id": camp.id,
            "campaign_id": camp.id,
            "title": camp.title,
            "subject": camp.context.subject,
            "objective": camp.context.objective,
            "language": camp.context.language,
            "platforms": camp.context.platforms,
            "asset_count": len(camp.assets),
            "status": camp.status,
            "created_at": camp.created_at,
            "updated_at": camp.updated_at
        })

    return sorted(history, key=lambda x: x["created_at"], reverse=True)
