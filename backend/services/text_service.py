import json
import logging
from typing import Dict, Any, List, Optional
from backend.config import settings
from backend.models.context import CampaignContext

logger = logging.getLogger(__name__)

class TextService:
    def __init__(self):
        self.groq_client = None
        if not settings.is_demo_mode and settings.GROQ_API_KEY:
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
            except Exception as e:
                logger.warning(f"Could not initialize Groq client in TextService: {e}")

    async def generate_platform_copy(
        self,
        platform: str,
        context: CampaignContext,
        target_language: str = "English",
        refinement_instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates platform-adapted copy honoring context, target language, and tone.
        """
        if self.groq_client:
            try:
                system_prompt = (
                    f"You are the Veyra AI Creative Copywriter specializing in {platform}. "
                    f"You must generate natural, culturally authentic copy in '{target_language}'. "
                    f"Follow platform conventions:\n"
                    f"- Instagram: Visual-first hook, punchy body, curated hashtags, clear link-in-bio CTA.\n"
                    f"- LinkedIn: Professional, authoritative, thought-leadership opening, structured bullet points, enterprise CTA.\n"
                    f"- YouTube Shorts: Dynamic punchy intro, rapid script lines, subscribe/register CTA.\n"
                    f"Never translate literally; adapt culturally and authentically.\n"
                    "Respond with a JSON object: {\n"
                    '  "hook": "Compelling first line",\n'
                    '  "content": "Full formatted post body",\n'
                    '  "hashtags": ["#tag1", "#tag2"],\n'
                    '  "call_to_action": "Specific CTA sentence"\n'
                    "}"
                )
                user_msg = (
                    f"Campaign Subject: {context.subject}\n"
                    f"Objective: {context.objective}\n"
                    f"Target Audience: {context.audience}\n"
                    f"Tone: {', '.join(context.tone)}\n"
                    f"Target Language: {target_language}\n"
                    f"Brand Guidelines: {json.dumps(context.brand)}\n"
                )
                if refinement_instructions:
                    user_msg += f"\nHuman Refinement Notes: {refinement_instructions}\n"

                completion = self.groq_client.chat.completions.create(
                    model=settings.TEXT_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_msg}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.7
                )
                result = json.loads(completion.choices[0].message.content)
                result["character_count"] = len(result.get("content", ""))
                return result
            except Exception as e:
                logger.error(f"Groq copy generation failed, using high-fidelity fallback: {e}")

        # High-Fidelity Context-Aware Fallback Engine
        if platform.lower() == "instagram":
            if "tamil" in target_language.lower():
                hook = "மாணவர்களின் புதுமை படைப்புகளை உலகிற்கு காட்டும் நேரம் இது! ⚡🚀"
                content = (
                    f"மாணவர்களின் புதுமை படைப்புகளை உலகிற்கு காட்டும் நேரம் இது! ⚡🚀\n\n"
                    f"{context.subject} — உங்கள் கனவுகளை நிஜமாக்கும் பிரம்மாண்ட படைப்பு மேடை!\n\n"
                    f"🔹 இலக்கு: {context.objective}\n"
                    f"🔹 AI & நவீன தொழில்நுட்பத் துறையின் சிறந்த வழிகாட்டிகள்\n"
                    f"🔹 கவர்ச்சிகரமான பரிசுகள் மற்றும் தொழில் வாய்ப்புகள்\n\n"
                    f"கோடிங், வடிவமைப்பு, புதுமையான திட்டங்கள் — உங்கள் திறமைக்கு தகுந்த அங்கீகாரம் பெற இன்றே இணையுங்கள்!\n\n"
                    f"இப்போதே பதிவு செய்யுங்கள்! லிங்க் பயோவில் உள்ளது ⬇️"
                )
                cta = "பயோவில் உள்ள லிங்க் மூலம் இப்போதே முன்பதிவு செய்யுங்கள்! (Link in Bio)"
                tags = ["#VeyraAI", "#TamilTech", "#Innovation", "#Students", "#NextGenTech"]
            elif "hindi" in target_language.lower():
                hook = "तकनीक और नवाचार की दुनिया में नया इतिहास रचने का समय आ गया है! 🚀💡"
                content = (
                    f"तकनीक और नवाचार की दुनिया में नया इतिहास रचने का समय आ गया है! 🚀💡\n\n"
                    f"{context.subject} — जहाँ आपकी प्रतिभा को मिलेगा एक वैश्विक मंच!\n\n"
                    f"🔹 उद्देश्य: {context.objective}\n"
                    f"🔹 उद्योग विशेषज्ञों और मेंटर्स का सीधा मार्गदर्शन\n"
                    f"🔹 आकर्षक नकद पुरस्कार और करियर के शानदार अवसर\n\n"
                    f"सीटें सीमित हैं। आज ही अपनी टीम के साथ रजिस्टर करें!"
                )
                cta = "बायो में दिए गए लिंक पर क्लिक करें और तुरंत रजिस्टर करें! (Link in Bio)"
                tags = ["#VeyraAI", "#TechIndia", "#InnovationHindi", "#Engineering", "#BuildTheFuture"]
            else:
                hook = f"Unleashing the next frontier: {context.subject}! 🚀✨"
                content = (
                    f"Unleashing the next frontier: {context.subject}! 🚀✨\n\n"
                    f"Designed specifically for {context.audience}. We are bringing together builders, designers, and innovators to {context.objective.lower()}.\n\n"
                    f"✨ What to expect:\n"
                    f"• Cutting-edge development sprints & elite mentoring\n"
                    f"• Transformative career pipelines & prize milestones\n"
                    f"• Hands-on immersion with next-gen AI tools\n\n"
                    f"Spots are limited. Secure your entry today!"
                )
                cta = "Tap the link in our bio to apply now! 🔗"
                tags = ["#VeyraAI", "#TechCreators", "#FutureBuilders", "#InnovationSprint"]

        elif platform.lower() == "linkedin":
            if "tamil" in target_language.lower():
                hook = f"தொழில்நுட்ப உலகில் புதிய புரட்சியை உருவாக்க தயாரா? — {context.subject} 🚀"
                content = (
                    f"தொழில்நுட்ப உலகில் புதிய புரட்சியை உருவாக்க தயாரா? — {context.subject} 🚀\n\n"
                    f"எங்களின் முதன்மை நோக்கம்: {context.objective}.\n\n"
                    f"{context.audience} க்காக வடிவமைக்கப்பட்ட இந்த நிகழ்வு, முன்னணி பொறியாளர்கள் மற்றும் நிறுவனங்களுடன் நேரடியாக இணையும் வாய்ப்பை வழங்குகிறது.\n\n"
                    f"முக்கிய சிறப்பம்சங்கள்:\n"
                    f"• துறைசார் வல்லுநர்களின் நேரடி வழிகாட்டுதல்\n"
                    f"• நடைமுறைத் திட்டங்களை உருவாக்கும் நேரடி அனுபவம்\n"
                    f"• தனித்துவமான நெட்வொர்க்கிங் மற்றும் வேலைவாய்ப்பு வாய்ப்புகள்\n\n"
                    f"இன்றே விண்ணப்பித்து உங்கள் தொழில்முறை பயணத்தை அடுத்த கட்டத்திற்கு கொண்டு செல்லுங்கள்."
                )
                cta = "அதிகாரப்பூர்வ இணைப்பைப் பார்வையிடவும் மற்றும் பதிவு செய்யவும்."
                tags = ["#VeyraAI", "#TechLeadership", "#EngineeringTamil", "#CareerGrowth"]
            elif "hindi" in target_language.lower():
                hook = f"क्या आप अगली पीढ़ी की तकनीकी क्रांति का नेतृत्व करने के लिए तैयार हैं? — {context.subject} 🚀"
                content = (
                    f"क्या आप अगली पीढ़ी की तकनीकी क्रांति का नेतृत्व करने के लिए तैयार हैं? — {context.subject} 🚀\n\n"
                    f"हमारा प्राथमिक उद्देश्य: {context.objective}।\n\n"
                    f"{context.audience} के लिए तैयार किया गया यह मंच आपको शीर्ष उद्योग विशेषज्ञों से जुड़ने का सुनहरा अवसर देता है।\n\n"
                    f"मुख्य आकर्षण:\n"
                    f"• व्यावहारिक तकनीकी नवाचार और मार्गदर्शन\n"
                    f"• प्रतिष्ठित उद्योग प्रमाणन और करियर के अवसर\n"
                    f"• उद्योग जगत के दिग्गजों से सीधे संवाद\n\n"
                    f"आज ही रजिस्टर करें और अपने करियर को एक नई दिशा दें।"
                )
                cta = "आधिकारिक पोर्टल पर जाएँ और आज ही आवेदन करें।"
                tags = ["#VeyraAI", "#TechLeadership", "#HindiTech", "#CareerAcceleration"]
            else:
                hook = f"Pioneering the future of intelligent systems: {context.subject} 🚀"
                content = (
                    f"Pioneering the future of intelligent systems: {context.subject} 🚀\n\n"
                    f"We are excited to announce our flagship initiative focused on {context.objective.lower()}.\n\n"
                    f"Curated specifically for {context.audience}, this initiative provides direct access to industry leaders, principal architects, and production-grade tools.\n\n"
                    f"Key Highlights:\n"
                    f"• Hands-on implementation of autonomous models and distributed systems\n"
                    f"• 1-on-1 mentorship with industry pioneers\n"
                    f"• Direct recruiting fast-tracks for high-performing teams\n\n"
                    f"Registrations are officially open."
                )
                cta = "Explore the full agenda and submit your application today."
                tags = ["#VeyraAI", "#SoftwareEngineering", "#EnterpriseTech", "#TechLeadership"]

        else: # YouTube Shorts / General
            hook = f"Don't miss out on {context.subject}! 💥"
            content = (
                f"30 seconds to change everything: {context.subject}.\n"
                f"Built for {context.audience} to {context.objective.lower()}.\n"
                f"Watch the full breakdown and link below to join!"
            )
            cta = "Subscribe and join the community link below!"
            tags = ["#VeyraAI", "#Shorts", "#TechTrending"]

        return {
            "hook": hook,
            "content": content,
            "hashtags": tags,
            "call_to_action": cta,
            "character_count": len(content)
        }

text_service = TextService()
