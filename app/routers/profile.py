from typing import Optional

from fastapi import APIRouter, Query

from ..api.riot import get_entries_for_summoner, get_matches, get_summoner_by_name
from ..consts import PLATFORM_TO_REGION
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
    summoner = await get_summoner_by_name(summoner_name, platform)
    summoner["other_queues"] = []
    summoner["profile_icon_url"] = (
        "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data"
        f"/global/default/v1/profile-icons/{summoner['profileIconId']}.jpg"
    )

    entries = await get_entries_for_summoner(summoner["id"], platform)
    for e in entries:
        if e["queueType"] == "RANKED_TFT":
            summoner.update(e)
        else:
            summoner["other_queues"].append(e)

    return summoner


@router.get("/{platform}/{summoner_name}/matches")
async def list_matches(
    platform: PLATFORMS,
    summoner_name: Homie,
    other_summoner: Optional[list[str]] = Query(None),
):
    result = None
    other_summoner = other_summoner or []
    for summ in [summoner_name, *other_summoner]:
        summoner = await get_summoner_by_name(summ, platform)
        matches = await get_matches(summoner["puuid"], PLATFORM_TO_REGION[platform])
        result = set(matches) if result is None else result.intersection(matches)
    return sorted(result, reverse=True)
