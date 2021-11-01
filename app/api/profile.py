from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from ..exceptions import SummonerNotFoundException
from ..literals import PLATFORMS
from ..models.profile import Homie, ProfileResponseSchema
from .riot import get_entries_for_summoner, get_summoner_by_name

router = APIRouter()


@router.get("/{platform}/{summoner_name}", response_model=ProfileResponseSchema)
async def get_profile(platform: PLATFORMS, summoner_name: Homie):
    try:
        summoner = await get_summoner_by_name(summoner_name, platform)
        entry = await get_entries_for_summoner(summoner["id"], platform)
        summoner.update(entry[0])
    except SummonerNotFoundException:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Summoner not found"
        )

    return summoner
