from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from ..exceptions import InvalidAPIKeyException, SummonerNotFoundException
from ..literals import PLATFORMS
from ..models.profile import Homie, ProfileResponseSchema
from .riot import get_entries_for_summoner, get_summoner_by_name

router = APIRouter()


@router.get("/{platform}/{summoner_name}", response_model=ProfileResponseSchema)
async def get_profile(platform: PLATFORMS, summoner_name: Homie):
    try:
        summoner = await get_summoner_by_name(summoner_name, platform)
        entries = await get_entries_for_summoner(summoner["id"], platform)
        for e in entries:
            if e["queueType"] != "RANKED_TFT":
                continue
            summoner.update(e)

    except SummonerNotFoundException:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Summoner not found"
        )
    except InvalidAPIKeyException:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY, detail="Invalid API Key"
        )

    return summoner
