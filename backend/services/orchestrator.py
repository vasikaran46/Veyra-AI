import uuid
import asyncio
import datetime
import logging
from typing import Dict, Any, List, Optional
from backend.models.context import CampaignContext
from backend.models.asset import Asset, AssetType, AssetStatus
from backend.models.campaign import Campaign, ContentStrategyPlan, GenerationJobResponse
from backend.services.context_engine import context_engine
from backend.services.model_router import model_router
from backend.utils.demo_data import get_default_hackathon_campaign

logger = logging.getLogger(__name__)

# Global in-memory storage for campaigns and active jobs
CAMPAIGNS_STORE: Dict[str, Campaign] = {}
JOBS_STORE: Dict[str, Dict[str, Any]] = {}

# Preload default hackathon campaign for instant demo exploration
default_camp = get_default_hackathon_campaign()
CAMPAIGNS_STORE[default_camp.id] = default_camp
CAMPAIGNS_STORE["default"] = default_camp

STEPS_DEFINITION = [
    {"index": 0, "name": "Understanding context", "description": "Extracting core marketing intent, tone, audience & constraints"},
    {"index": 1, "name": "Building content strategy", "description": "Formulating coordinated cross-platform deployment narrative"},
    {"index": 2, "name": "Adapting for platforms", "description": "Tailoring hooks, dimensions, and specifications per channel"},
    {"index": 3, "name": "Generating text", "description": "Synthesizing authentic localized captions and announcements"},
    {"index": 4, "name": "Generating visual", "description": "Rendering high-fidelity imagery with localized typographic overlay"},
    {"index": 5, "name": "Generating video", "description": "Composing kinetic 9:16 vertical video storyboard & bilingual subtitles"},
    {"index": 6, "name": "Generating audio", "description": "Synthesizing regional voice-over audio track & waveform profiles"},
    {"index": 7, "name": "Preparing review", "description": "Assembling unified campaign package for human-in-the-loop validation"}
]

class AIOrchestrator:
    def __init__(self):
        pass

    def create_job(self, campaign_id: str) -> str:
        job_id = f"job_{uuid.uuid4().hex[:10]}"
        steps = []
        for s in STEPS_DEFINITION:
            steps.append({
                "index": s["index"],
                "name": s["name"],
                "description": s["description"],
                "status": "pending"  # pending, in_progress, completed, failed
            })
        JOBS_STORE[job_id] = {
            "job_id": job_id,
            "campaign_id": campaign_id,
            "status": "QUEUED",
            "step_index": 0,
            "current_step": STEPS_DEFINITION[0]["name"],
            "total_steps": len(STEPS_DEFINITION),
            "steps": steps,
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "error": None
        }
        return job_id

    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        job = JOBS_STORE.get(job_id)
        if not job:
            return None
        camp = CAMPAIGNS_STORE.get(job["campaign_id"])
        job_copy = dict(job)
        job_copy["campaign"] = camp
        return job_copy

    async def run_generation_pipeline(
        self,
        job_id: str,
        prompt: str,
        campaign_id: Optional[str] = None,
        overrides: Optional[Dict[str, Any]] = None,
        brand_data: Optional[Dict[str, Any]] = None
    ):
        """
        Executes the 8-stage asynchronous orchestration workflow.
        """
        logger.info(f"Starting Veyra orchestration for job {job_id}")
        job = JOBS_STORE[job_id]
        job["status"] = "PROCESSING"
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        try:
            # Step 1: Understanding context
            job["step_index"] = 0
            job["current_step"] = STEPS_DEFINITION[0]["name"]
            job["steps"][0]["status"] = "in_progress"
            await asyncio.sleep(0.6)

            context = await context_engine.extract_context(
                prompt=prompt,
                overrides=overrides,
                brand_data=brand_data
            )
            job["steps"][0]["status"] = "completed"

            # Step 2: Building content strategy
            job["step_index"] = 1
            job["current_step"] = STEPS_DEFINITION[1]["name"]
            job["steps"][1]["status"] = "in_progress"
            await asyncio.sleep(0.6)

            strategy = ContentStrategyPlan(
                summary=(
                    f"A multi-channel growth narrative for '{context.subject}' engineered to {context.objective.lower()}. "
                    f"Orchestrating regional authentic vernacular with prestigious professional outreach."
                ),
                pillars=[
                    f"Empowerment & High Value ({context.subject})",
                    f"Skill Mastery & Recognition for {context.audience}",
                    f"Clear conversion action with urgent registration milestones"
                ],
                platform_roles={
                    "Instagram": "Viral cultural hook with high-impact visual poster & kinetic reel preview",
                    "LinkedIn": "Deep technical credibility, career impact, and institutional partner reach",
                    "YouTube Shorts": "High-velocity 30s teaser with regional voice-over & synchronized subtitles"
                },
                timeline_milestones=[
                    "Phase 1: Momentum Teaser & Community Announcement",
                    "Phase 2: Challenge / Value Deep-Dive & Visual Posters",
                    "Phase 3: Countdown Sprint & Final Registration Push"
                ],
                multilingual_strategy=f"Deploys native vernacular for emotional engagement ({context.language}) coupled with global technical English."
            )
            job["steps"][1]["status"] = "completed"

            # Step 3: Adapting for platforms
            job["step_index"] = 2
            job["current_step"] = STEPS_DEFINITION[2]["name"]
            job["steps"][2]["status"] = "in_progress"
            await asyncio.sleep(0.5)
            job["steps"][2]["status"] = "completed"

            target_camp_id = campaign_id or f"camp_{uuid.uuid4().hex[:8]}"
            job["campaign_id"] = target_camp_id
            assets: List[Asset] = []

            # Step 4: Generating text
            job["step_index"] = 3
            job["current_step"] = STEPS_DEFINITION[3]["name"]
            job["steps"][3]["status"] = "in_progress"
            await asyncio.sleep(0.7)

            # 4a. Instagram text (Tamil or primary regional language)
            ig_lang = "Tamil" if "tamil" in context.language.lower() else ("Hindi" if "hindi" in context.language.lower() else "English")
            ig_text_res = await model_router.generate_text(
                platform="Instagram",
                context=context,
                target_language=ig_lang
            )
            asset_ig_text = Asset(
                id=f"ast_{uuid.uuid4().hex[:8]}",
                campaign_id=target_camp_id,
                type=AssetType.TEXT,
                title=f"Instagram Launch Caption ({ig_lang})",
                platform="Instagram",
                language=ig_lang,
                status=AssetStatus.READY_FOR_REVIEW,
                hook=ig_text_res.get("hook"),
                content=ig_text_res.get("content"),
                character_count=ig_text_res.get("character_count"),
                hashtags=ig_text_res.get("hashtags", []),
                call_to_action=ig_text_res.get("call_to_action"),
                created_at=now,
                updated_at=now
            )
            assets.append(asset_ig_text)

            # 4b. LinkedIn text (English)
            li_text_res = await model_router.generate_text(
                platform="LinkedIn",
                context=context,
                target_language="English"
            )
            asset_li_text = Asset(
                id=f"ast_{uuid.uuid4().hex[:8]}",
                campaign_id=target_camp_id,
                type=AssetType.TEXT,
                title="LinkedIn Executive Announcement (English)",
                platform="LinkedIn",
                language="English",
                status=AssetStatus.READY_FOR_REVIEW,
                hook=li_text_res.get("hook"),
                content=li_text_res.get("content"),
                character_count=li_text_res.get("character_count"),
                hashtags=li_text_res.get("hashtags", []),
                call_to_action=li_text_res.get("call_to_action"),
                created_at=now,
                updated_at=now
            )
            assets.append(asset_li_text)
            job["steps"][3]["status"] = "completed"

            # Step 5: Generating visual
            job["step_index"] = 4
            job["current_step"] = STEPS_DEFINITION[4]["name"]
            job["steps"][4]["status"] = "in_progress"
            await asyncio.sleep(0.8)

            img_res = await model_router.generate_image(
                prompt=f"Graphic design promotional poster for {context.subject}. Modern minimalist glassmorphic aesthetic with electric violet highlights and cyan telemetry.",
                aspect_ratio="4:5 (1080x1350)",
                context=context,
                overlay_language=ig_lang
            )
            asset_image = Asset(
                id=f"ast_{uuid.uuid4().hex[:8]}",
                campaign_id=target_camp_id,
                type=AssetType.IMAGE,
                title="Official Visual Poster",
                platform="Instagram & LinkedIn",
                language=f"{ig_lang} & English",
                status=AssetStatus.READY_FOR_REVIEW,
                media_url=img_res.get("media_url"),
                aspect_ratio=img_res.get("aspect_ratio"),
                prompt=img_res.get("prompt"),
                model_name=img_res.get("model_name"),
                overlay_text=img_res.get("overlay_text"),
                overlay_language=img_res.get("overlay_language"),
                created_at=now,
                updated_at=now
            )
            assets.append(asset_image)
            job["steps"][4]["status"] = "completed"

            # Step 6: Generating video
            job["step_index"] = 5
            job["current_step"] = STEPS_DEFINITION[5]["name"]
            job["steps"][5]["status"] = "in_progress"
            await asyncio.sleep(0.8)

            vid_res = await model_router.generate_video(
                prompt=f"Vertical 9:16 kinetic video frame for {context.subject} with energetic motion and ambient futuristic lighting.",
                context=context,
                language=ig_lang
            )
            asset_video = Asset(
                id=f"ast_{uuid.uuid4().hex[:8]}",
                campaign_id=target_camp_id,
                type=AssetType.VIDEO,
                title=f"30s Kinetic Reel ({ig_lang} Voice + Dual Subtitles)",
                platform="YouTube Shorts & Reels",
                language=f"{ig_lang} (Voice) + Subtitles",
                status=AssetStatus.READY_FOR_REVIEW,
                media_url=vid_res.get("media_url"),
                aspect_ratio=vid_res.get("aspect_ratio"),
                duration_seconds=vid_res.get("duration_seconds"),
                prompt=vid_res.get("prompt"),
                model_name=vid_res.get("model_name"),
                video_storyboard=vid_res.get("storyboard", []),
                subtitles=vid_res.get("subtitles", []),
                created_at=now,
                updated_at=now
            )
            assets.append(asset_video)
            job["steps"][5]["status"] = "completed"

            # Step 7: Generating audio
            job["step_index"] = 6
            job["current_step"] = STEPS_DEFINITION[6]["name"]
            job["steps"][6]["status"] = "in_progress"
            await asyncio.sleep(0.7)

            audio_res = await model_router.generate_audio(
                context=context,
                language=ig_lang
            )
            asset_audio = Asset(
                id=f"ast_{uuid.uuid4().hex[:8]}",
                campaign_id=target_camp_id,
                type=AssetType.AUDIO,
                title=f"Promotional Audio Voice-Over ({ig_lang})",
                platform="YouTube Shorts & Reels",
                language=ig_lang,
                status=AssetStatus.READY_FOR_REVIEW,
                voice_name=audio_res.get("voice_name"),
                audio_duration=audio_res.get("audio_duration"),
                audio_transcript=audio_res.get("audio_transcript"),
                waveform_data=audio_res.get("waveform_data", []),
                model_name=audio_res.get("model_name"),
                created_at=now,
                updated_at=now
            )
            assets.append(asset_audio)
            job["steps"][6]["status"] = "completed"

            # Step 8: Preparing review
            job["step_index"] = 7
            job["current_step"] = STEPS_DEFINITION[7]["name"]
            job["steps"][7]["status"] = "in_progress"
            await asyncio.sleep(0.5)

            new_campaign = Campaign(
                id=target_camp_id,
                title=context.subject,
                status="IN_REVIEW",
                context=context,
                strategy_plan=strategy,
                assets=assets,
                created_at=now,
                updated_at=now,
                notes=f"Generated via Super Prompt: {prompt}"
            )
            CAMPAIGNS_STORE[target_camp_id] = new_campaign
            CAMPAIGNS_STORE["default"] = new_campaign

            job["steps"][7]["status"] = "completed"
            job["status"] = "COMPLETED"
            job["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            logger.info(f"Veyra orchestration completed successfully for {target_camp_id}")

        except Exception as e:
            logger.error(f"Error during orchestration pipeline: {e}", exc_info=True)
            job["status"] = "FAILED"
            job["error"] = str(e)
            job["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

orchestrator = AIOrchestrator()
