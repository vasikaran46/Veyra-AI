import json
import logging
from typing import Dict, Any, Optional
from backend.config import settings
from backend.models.context import CampaignContext

logger = logging.getLogger(__name__)

class ContextEngine:
    def __init__(self):
        self.groq_client = None
        if not settings.is_demo_mode and settings.GROQ_API_KEY:
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
            except Exception as e:
                logger.warning(f"Could not initialize Groq client: {e}")

    async def extract_context(
        self,
        prompt: str,
        overrides: Optional[Dict[str, Any]] = None,
        brand_data: Optional[Dict[str, Any]] = None
    ) -> CampaignContext:
        """
        Extracts structured multi-dimensional campaign context from a natural language prompt.
        Uses Groq if available, or context-aware intelligent heuristic parser.
        """
        overrides = overrides or {}
        brand_data = brand_data or {}

        # If Groq is active and not forced into demo mode:
        if self.groq_client:
            try:
                system_prompt = (
                    "You are the Veyra AI Context Engine. Your job is to analyze the user's campaign prompt "
                    "and extract a structured creative intelligence context. Respond ONLY with valid JSON "
                    "matching this schema:\n"
                    "{\n"
                    '  "subject": "Clear concise subject/title",\n'
                    '  "objective": "Primary marketing/growth objective",\n'
                    '  "audience": "Specific target audience profile",\n'
                    '  "platforms": ["Instagram", "LinkedIn", "YouTube Shorts"],\n'
                    '  "tone": ["Energetic", "Professional"],\n'
                    '  "language": "Primary language, e.g. English or Tamil or Hindi",\n'
                    '  "region": "Target region, e.g. India or Global",\n'
                    '  "content_types": ["Text", "Image", "Video", "Audio"]\n'
                    "}"
                )
                completion = self.groq_client.chat.completions.create(
                    model=settings.TEXT_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"User Prompt: {prompt}\nBrand: {json.dumps(brand_data)}"}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.3
                )
                data = json.loads(completion.choices[0].message.content)
                data["brand"] = brand_data
                for k, v in overrides.items():
                    if v is not None:
                        data[k] = v
                return CampaignContext(**data)
            except Exception as e:
                logger.error(f"Groq context extraction failed, falling back to heuristic engine: {e}")

        # Intelligent heuristic extraction (Demo / Fallback Mode)
        lower_prompt = prompt.lower()
        
        # 1. Subject extraction
        subject = prompt.strip()
        if "create a promotional campaign for" in lower_prompt:
            subject = prompt.split("campaign for", 1)[-1].strip().capitalize()
        elif "create a campaign for" in lower_prompt:
            subject = prompt.split("campaign for", 1)[-1].strip().capitalize()

        # 2. Objective detection
        objective = "Drive high engagement and active audience registrations"
        if "hackathon" in lower_prompt:
            objective = "Maximize engineering student registrations & showcase high-value prize pool"
        elif "product" in lower_prompt or "launch" in lower_prompt:
            objective = "Generate pre-orders and brand awareness for product debut"
        elif "workshop" in lower_prompt or "webinar" in lower_prompt:
            objective = "Secure attendee reservations and educate target community"

        # 3. Audience detection
        audience = "Engineering students, developers, UI/UX designers, and tech creators"
        if "student" in lower_prompt or "college" in lower_prompt or "engineering" in lower_prompt:
            audience = "College engineering undergraduates, tech club members, and young innovators"
        elif "enterprise" in lower_prompt or "b2b" in lower_prompt:
            audience = "Tech executives, engineering directors, and product leaders"
        elif "designer" in lower_prompt or "creative" in lower_prompt:
            audience = "Digital creators, art directors, and creative technologists"

        # 4. Platforms
        platforms = overrides.get("platforms") or ["Instagram", "LinkedIn", "YouTube Shorts"]

        # 5. Tone
        tone = overrides.get("tone") or ["Energetic", "Professional", "High-Impact"]
        if "playful" in lower_prompt:
            tone = ["Playful", "Bold", "Casual"]
        elif "corporate" in lower_prompt or "formal" in lower_prompt:
            tone = ["Authoritative", "Polished", "Corporate"]

        # 6. Language & Region
        language = overrides.get("language") or "English & Tamil"
        region = overrides.get("region") or "India / Global"
        content_types = overrides.get("content_types") or ["Text", "Image", "Video", "Audio"]

        return CampaignContext(
            subject=subject,
            objective=objective,
            audience=audience,
            platforms=platforms,
            tone=tone,
            language=language,
            region=region,
            brand=brand_data,
            content_types=content_types,
            extra_instructions=overrides.get("extra_instructions")
        )

context_engine = ContextEngine()
