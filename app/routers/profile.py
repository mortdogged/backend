from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from ..api.riot import get_entries_for_summoner, get_summoner_by_name
from ..exceptions import InvalidAPIKeyException, SummonerNotFoundException
from ..literals import PLATFORMS
from ..models import ErrorResponseSchema, Homie, ProfileResponseSchema

router = APIRouter()


@router.get(
    "/{platform}/{summoner_name}",
    response_model=ProfileResponseSchema,
    responses={
        404: {"model": ErrorResponseSchema},
        502: {"model": ErrorResponseSchema},
    },
)
async def get_profile(platform: PLATFORMS, summoner_name: Homie):
    try:
        summoner = await get_summoner_by_name(summoner_name, platform)
        print(summoner)
        summoner["profile_icon_url"] = (
            "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data"
            f"/global/default/v1/profile-icons/{summoner['profileIconId']}.jpg"
        )

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
