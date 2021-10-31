from fastapi import APIRouter

from ..literals import PLATFORMS
from ..models.profile import ProfileResponseSchema
from .riot import get_entries_for_summoner, get_summoner_by_name

router = APIRouter()


@router.get("/{platform}/{summoner_name}", response_model=ProfileResponseSchema)
async def get_profile(
    platform: PLATFORMS,
    summoner_name: str,
):
    summoner = await get_summoner_by_name(summoner_name, platform)
    entry = await get_entries_for_summoner(summoner["id"], platform)

    summoner.update(entry[0])
    return summoner
