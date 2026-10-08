import uuid
import datetime
from typing import Dict, Any, List
from backend.models.asset import Asset, AssetType, AssetStatus
from backend.models.context import CampaignContext
from backend.models.campaign import Campaign, ContentStrategyPlan

def get_default_hackathon_campaign() -> Campaign:
    camp_id = f"camp_{uuid.uuid4().hex[:8]}"
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    context = CampaignContext(
        subject="HACK//NEXUS 2025: Build the Intelligent Future",
        objective="Drive 1,200+ high-caliber engineering student registrations & sponsor engagement",
        audience="Undergraduate & graduate engineering students, developers, UI/UX designers, AI hobbyists",
        platforms=["Instagram", "LinkedIn", "YouTube Shorts"],
        tone=["Energetic", "Professional", "High-Impact", "Inspiring"],
        language="English & Tamil",
        region="India (Tamil Nadu & Pan-India)",
        brand={
            "name": "Nexus Innovations Lab",
            "primary_color": "#7C3AED",
            "secondary_color": "#06B6D4"
        },
        content_types=["Text", "Image", "Video", "Audio"]
    )
    
    strategy = ContentStrategyPlan(
        summary="A coordinated multimodal blitz combining regional cultural resonance (Tamil) on high-velocity social channels (Instagram, YouTube Shorts) with high-credibility career and technical prestige (English) on professional networks (LinkedIn).",
        pillars=[
            "Innovation & Real-World Impact (Build autonomous AI agents & scalable cloud architectures)",
            "Prizes & Industry Access (₹1,50,000 Cash Pool + Direct interviews with top tech firms)",
            "Community & Mentorship (48-hour collaborative sprint with leading mentors)"
        ],
        platform_roles={
            "Instagram": "Viral cultural hook in Tamil + high-octane visual cyber poster + dynamic reel preview",
            "LinkedIn": "Deep technical credibility, judge lineup, enterprise partner announcements, and portfolio boost",
            "YouTube Shorts": "High-adrenaline 30s teaser with regional Tamil voice-over and dual-language subtitles"
        },
        timeline_milestones=[
            "Phase 1: The Teaser Drop (Instagram Reel + YouTube Short with Tamil Voice-Over)",
            "Phase 2: The Core Challenge Reveal & Poster (Instagram High-Res + LinkedIn Technical Brief)",
            "Phase 3: Registration Countdown & FAQ Series"
        ],
        multilingual_strategy="Primary visual assets utilize English technical branding with crisp Tamil localized typography overlays. Social copy is delivered natively in Tamil for emotional connection, complemented by polished English for professional networks."
    )
    
    # 1. Instagram Post & Tamil Caption
    asset_ig_text = Asset(
        id=f"ast_{uuid.uuid4().hex[:8]}",
        campaign_id=camp_id,
        type=AssetType.TEXT,
        title="Instagram Launch Caption (Tamil)",
        platform="Instagram",
        language="Tamil",
        status=AssetStatus.READY_FOR_REVIEW,
        hook="மாணவர்களின் புதுமை படைப்புகளை உலகிற்கு காட்டும் நேரம் இது! ⚡🚀",
        content=(
            "மாணவர்களின் புதுமை படைப்புகளை உலகிற்கு காட்டும் நேரம் இது! ⚡🚀\n\n"
            "HACK//NEXUS 2025 — உங்கள் கனவுகளை நிஜமாக்கும் 48 மணிநேர பிரம்மாண்ட Hackathon!\n\n"
            "🔹 ₹1,50,000+ ரொக்கப் பரிசுகள்\n"
            "🔹 AI & Cloud துறையின் தலைசிறந்த வழிகாட்டிகள்\n"
            "🔹 நேரடி வேலைவாய்ப்பு மற்றும் இன்டர்ன்ஷிப் வாய்ப்புகள்\n\n"
            "கோடிங், டிசைனிங், அல்லது புதுமையான யோசனைகள் — உங்களிடம் தீர்வு இருந்தால், மேடை உங்களுடையது!\n\n"
            "இடங்கள் வேகமாக நிரம்புகின்றன! உடனடியாக பதிவு செய்யுங்கள் ⬇️"
        ),
        character_count=448,
        hashtags=["#HackNexus2025", "#TamilTech", "#HackathonIndia", "#CodingTamil", "#EngineeringStudents", "#VeyraAI"],
        call_to_action="பயோவில் உள்ள லிங்க் மூலம் இப்போதே முன்பதிவு செய்யுங்கள்! (Link in Bio)",
        created_at=now,
        updated_at=now
    )
    
    # 2. Instagram Poster (Image Asset)
    asset_poster = Asset(
        id=f"ast_{uuid.uuid4().hex[:8]}",
        campaign_id=camp_id,
        type=AssetType.IMAGE,
        title="Official Cyber-Minimalist Event Poster",
        platform="Instagram",
        language="Tamil & English",
        status=AssetStatus.READY_FOR_REVIEW,
        media_url="/assets/hackathon_poster.jpg",
        aspect_ratio="4:5 (1080x1350)",
        prompt="High-end graphic design promotional poster for a college hackathon titled 'HACK//NEXUS 2025: Build the Intelligent Future'. Cyber-minimalist aesthetic, vibrant holographic 3D wireframe geometric core, glowing electric violet and neon cyan light trails, dark obsidian glass textures, typography layout ready, sleek tech event poster design, highly detailed 8k.",
        model_name="Flux Schnell / Replicate",
        overlay_text="HACK//NEXUS 2025 — உங்கள் எதிர்காலத்தை இன்றே உருவாக்குங்கள்",
        overlay_language="Tamil",
        created_at=now,
        updated_at=now
    )
    
    # 3. LinkedIn Announcement (English)
    asset_li_text = Asset(
        id=f"ast_{uuid.uuid4().hex[:8]}",
        campaign_id=camp_id,
        type=AssetType.TEXT,
        title="LinkedIn Official Call for Builders (English)",
        platform="LinkedIn",
        language="English",
        status=AssetStatus.READY_FOR_REVIEW,
        hook="Ready to architect the next frontier of generative intelligence and distributed systems? 🚀",
        content=(
            "Ready to architect the next frontier of generative intelligence and distributed systems? 🚀\n\n"
            "Announcing HACK//NEXUS 2025 — where 1,200+ engineers, designers, and systems architects converge for an intensive 48-hour sprint to build production-grade solutions.\n\n"
            "Why participate?\n"
            "• ₹1,50,000+ Prize Pool & Fast-Track Interview pipelines with leading tech enterprises\n"
            "• Direct 1:1 mentorship from Principal Engineers and AI Research Leads\n"
            "• Tracks covering: Autonomous AI Agents, Resilient Infrastructure, and Multimodal Interfaces\n\n"
            "Whether you're pushing custom LoRA weights or scaling low-latency APIs, this is your arena.\n\n"
            "Registrations are officially open for university teams and independent builders."
        ),
        character_count=782,
        hashtags=["#HackNexus2025", "#SoftwareEngineering", "#GenerativeAI", "#TechLeadership", "#DeveloperCommunity"],
        call_to_action="Apply today via the official portal: hacknexus.dev/apply",
        created_at=now,
        updated_at=now
    )
    
    # 4. YouTube Shorts / Reel Video (Video Asset)
    asset_video = Asset(
        id=f"ast_{uuid.uuid4().hex[:8]}",
        campaign_id=camp_id,
        type=AssetType.VIDEO,
        title="30s High-Adrenaline Kinetic Teaser Reel",
        platform="YouTube Shorts",
        language="Tamil (Voice) + Dual Subtitles",
        status=AssetStatus.READY_FOR_REVIEW,
        media_url="/assets/video_thumbnail.jpg",
        aspect_ratio="9:16 (1080x1920)",
        duration_seconds=30,
        prompt="Vertical 9:16 video frame preview of a dynamic futuristic hackathon reel: energetic students collaborating around glowing holographic code monitors, sleek dark auditorium, motion blur light streaks, vibrant ambient cyan and purple lighting, cinematic 4k film still.",
        model_name="MiniMax Video-01 / Replicate",
        video_storyboard=[
            "00:00 - 00:05 | Opening Glitch & Obsidian Neon Title: HACK//NEXUS 2025",
            "00:05 - 00:15 | Fast montage: Late night coding, dual-screen setups, collaborative whiteboard brainstorms",
            "00:15 - 00:22 | Prize pool counter zooming to ₹1,50,000 with mentor showcase",
            "00:22 - 00:30 | Grand finale countdown clock and call to register"
        ],
        subtitles=[
            {
                "start": "00:01",
                "end": "00:05",
                "tamil": "உங்கள் திறமைக்கு ஒரு மாபெரும் சவால் காத்திருக்கிறது!",
                "english": "A massive challenge awaits your true technical potential!"
            },
            {
                "start": "00:06",
                "end": "00:14",
                "tamil": "48 மணிநேரம், 1200+ பொறியாளர்கள், புதிய எதிர்காலத்தை உருவாக்குங்கள்.",
                "english": "48 hours, 1,200+ engineers, shaping the intelligent future."
            },
            {
                "start": "00:15",
                "end": "00:22",
                "tamil": "₹1,50,000 ரொக்கப்பரிசுகளுடன் முன்னணி நிறுவனங்களின் அங்கீகாரம்!",
                "english": "₹1,50,000 cash rewards and direct enterprise mentorship!"
            },
            {
                "start": "00:23",
                "end": "00:30",
                "tamil": "இப்போதே பதிவு செய்யுங்கள்! HACK//NEXUS 2025.",
                "english": "Register right now! HACK//NEXUS 2025."
            }
        ],
        created_at=now,
        updated_at=now
    )
    
    # 5. Dynamic Audio Voice-Over (Audio Asset)
    asset_audio = Asset(
        id=f"ast_{uuid.uuid4().hex[:8]}",
        campaign_id=camp_id,
        type=AssetType.AUDIO,
        title="Promotional Audio Voice-Over (Tamil Energizer)",
        platform="YouTube Shorts & Reels",
        language="Tamil",
        status=AssetStatus.READY_FOR_REVIEW,
        voice_name="Karthik - Dynamic & Energetic Youth Accent",
        audio_duration=28.5,
        audio_transcript="மாணவர்களின் புதிய சிந்தனைகளை உலகறிய செய்ய வருகிறது HACK NEXUS 2025! 48 மணிநேரத்தில் உங்கள் தொழில்நுட்ப திறமையால் உலகை மாற்றுங்கள். ஒரு லட்சத்து ஐம்பதாயிரம் ரூபாய் பரிசுகள்! உடனடியாக இணையுங்கள்!",
        waveform_data=[0.12, 0.45, 0.78, 0.92, 0.65, 0.85, 0.40, 0.15, 0.58, 0.89, 0.95, 0.73, 0.61, 0.84, 0.98, 0.52, 0.35, 0.76, 0.88, 0.67, 0.42, 0.19, 0.63, 0.81, 0.75, 0.38, 0.12, 0.05],
        created_at=now,
        updated_at=now
    )
    
    return Campaign(
        id=camp_id,
        title="HACK//NEXUS 2025 Launch Campaign",
        status="IN_REVIEW",
        context=context,
        strategy_plan=strategy,
        assets=[asset_ig_text, asset_poster, asset_li_text, asset_video, asset_audio],
        created_at=now,
        updated_at=now,
        notes="Generated seamlessly through Veyra Context-Aware Engine."
    )
