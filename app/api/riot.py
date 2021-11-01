from httpx import AsyncClient

from ..config import get_settings
from ..exceptions import InvalidAPIKeyException, SummonerNotFoundException
from ..literals import PLATFORMS

BASE_URL = "https://{}.api.riotgames.com/tft"


async def get_summoner_by_name(name: str, platform: PLATFORMS):
    async with AsyncClient() as client:
        r = await client.get(
            f"{BASE_URL.format(platform)}/summoner/v1/summoners/by-name/{name}",
            headers={"X-Riot-Token": get_settings().api_key},
        )
    response = r.json()
    if response == {
        "status": {"message": "Data not found - summoner not found", "status_code": 404}
    }:
        raise SummonerNotFoundException
    elif response == {"status": {"message": "Forbidden", "status_code": 403}}:
        raise InvalidAPIKeyException
    return response


async def get_entries_for_summoner(summoner_id: str, platform: PLATFORMS):
    async with AsyncClient() as client:
        r = await client.get(
            f"{BASE_URL.format(platform)}/league/v1/entries/by-summoner/{summoner_id}",
            headers={"X-Riot-Token": get_settings().api_key},
        )
    return r.json()
