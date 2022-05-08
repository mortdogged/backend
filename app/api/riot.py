import json
from http import HTTPStatus

from httpx import AsyncClient

from ..config import get_cache, get_settings
from ..exceptions import InvalidAPIKeyException, SummonerNotFoundException
from ..literals import PLATFORMS, REGIONS

BASE_URL = "https://{}.api.riotgames.com/tft"


async def get_summoner_by_name(name: str, platform: PLATFORMS):
    response = get_cache().get(f"{name}-{platform}")
    if not response:
        async with AsyncClient() as client:
            r = await client.get(
                f"{BASE_URL.format(platform)}/summoner/v1/summoners/by-name/{name}",
                headers={"X-Riot-Token": get_settings().api_key},
            )
        response = r.json()
        get_cache().set(
            f"{name}-{platform}",
            json.dumps(response),
            ex=get_settings().cache_expired_time,
        )
    else:
        response = json.loads(response)

    if "status" in response:
        if response["status"]["status_code"] == HTTPStatus.NOT_FOUND:
            raise SummonerNotFoundException
        if response["status"]["status_code"] == HTTPStatus.FORBIDDEN:
            raise InvalidAPIKeyException

    return response


async def get_entries_for_summoner(summoner_id: str, platform: PLATFORMS):
    async with AsyncClient() as client:
        r = await client.get(
            f"{BASE_URL.format(platform)}/league/v1/entries/by-summoner/{summoner_id}",
            headers={"X-Riot-Token": get_settings().api_key},
        )
    return r.json()


async def get_matches(puuid: str, region: REGIONS):
    async with AsyncClient() as client:
        matches_returned = 1000
        r = await client.get(
            f"{BASE_URL.format(region)}/match/v1/matches/by-puuid/"
            f"{puuid}/ids?count={matches_returned}",
            headers={"X-Riot-Token": get_settings().api_key},
        )
    return r.json()
