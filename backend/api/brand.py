from fastapi import APIRouter
from backend.models.brand import BrandMemory

router = APIRouter(prefix="/api/brand", tags=["brand"])

ACTIVE_BRAND = BrandMemory()

@router.get("", response_model=BrandMemory)
async def get_brand():
    """Retrieve active brand memory configuration."""
    return ACTIVE_BRAND

@router.patch("", response_model=BrandMemory)
async def update_brand(updates: BrandMemory):
    """Update active brand memory parameters."""
    global ACTIVE_BRAND
    ACTIVE_BRAND = updates
    return ACTIVE_BRAND
