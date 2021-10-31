from httpx import AsyncClient

from ..config import get_settings

BASE_URL = "https://{platform}.api.riotgames.com/tft"


async def get_summoner_by_name(name: str, platform):
    async with AsyncClient() as client:
        r = await client.get(
            f"{BASE_URL.format(platform)}/summoner/v1/summoners/by-name/{name}",
            headers={"X-Riot-Token": get_settings().api_key},
        )
    return r.json()


async def get_entries_for_summoner(summoner_id: str, platform):
    async with AsyncClient() as client:
        r = await client.get(
            f"{BASE_URL.format(platform)}/league/v1/entries/by-summoner/{summoner_id}",
            headers={"X-Riot-Token": get_settings().api_key},
        )
    return r.json()
