from fastapi import APIRouter, BackgroundTasks, HTTPException
from backend.models.campaign import GenerationRequest, GenerationJobResponse
from backend.services.orchestrator import orchestrator, CAMPAIGNS_STORE

router = APIRouter(prefix="/api/generate", tags=["generation"])

@router.post("", response_model=GenerationJobResponse)
async def start_generation(req: GenerationRequest, background_tasks: BackgroundTasks):
    """
    Initiates asynchronous generation flow from a prompt.
    Returns a job_id for frontend polling of the 8-stage progress stepper.
    """
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    campaign_id = req.campaign_id or None
    job_id = orchestrator.create_job(campaign_id=campaign_id or "pending")

    overrides = {
        "language": req.language,
        "region": req.region,
        "platforms": req.platforms,
        "content_types": req.content_types,
        "tone": req.tone
    }

    # Launch generation pipeline in background task
    background_tasks.add_task(
        orchestrator.run_generation_pipeline,
        job_id=job_id,
        prompt=req.prompt,
        campaign_id=campaign_id,
        overrides=overrides,
        brand_data=None
    )

    job_data = orchestrator.get_job_status(job_id)
    return GenerationJobResponse(**job_data)

@router.get("/{job_id}", response_model=GenerationJobResponse)
async def get_generation_status(job_id: str):
    """Poll generation job status, current step, and assembled assets."""
    job_data = orchestrator.get_job_status(job_id)
    if not job_data:
        raise HTTPException(status_code=404, detail="Job not found")
    return GenerationJobResponse(**job_data)
