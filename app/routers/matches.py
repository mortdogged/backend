from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from ..api.riot import get_matches, get_summoner_by_name
from ..consts import PLATFORM_TO_REGION
from ..exceptions import InvalidAPIKeyException, SummonerNotFoundException
from ..literals import PLATFORMS
from ..models import Homie

router = APIRouter()


@router.get("/")
async def list_matches(platform: PLATFORMS, summoner_name: Homie):
    try:
        summoner = await get_summoner_by_name(summoner_name, platform)
        matches = await get_matches(summoner["puuid"], PLATFORM_TO_REGION[platform])
        return matches
    except SummonerNotFoundException:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Summoner not found"
        )
    except InvalidAPIKeyException:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY, detail="Invalid API Key"
        )
