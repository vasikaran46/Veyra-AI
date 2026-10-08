from typing import List, Optional
from pydantic import BaseModel, Field

class BrandMemory(BaseModel):
    id: str = Field("brand_default", description="Brand ID")
    name: str = Field("Veyra AI Labs", description="Brand or organization name")
    description: str = Field(
        "A pioneering developer intelligence and creative generative AI laboratory advancing human creativity.",
        description="Core brand premise"
    )
    logo_url: Optional[str] = Field(None, description="Logo URL or asset path")
    primary_color: str = Field("#7C3AED", description="Hex primary color")
    secondary_color: str = Field("#06B6D4", description="Hex secondary accent")
    background_tone: str = Field("#11141E", description="Warm obsidian / cream background")
    typography: str = Field("Geist & JetBrains Mono", description="Brand font stack")
    voice_tone: List[str] = Field(
        default_factory=lambda: ["Calm", "Intelligent", "Empowering", "Precision-focused"]
    )
    target_audience: str = Field(
        "Modern creators, engineers, strategists, and innovators.",
        description="Target persona"
    )
    guidelines: str = Field(
        "Maintain human dignity, clarity, and bold forward momentum. Never use cheap gimmicks or noisy cliches.",
        description="Rules of engagement"
    )
