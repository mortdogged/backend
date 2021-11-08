import httpx
import pytest

from app.api.riot import get_summoner_by_name
from app.exceptions import InvalidAPIKeyException, SummonerNotFoundException

# Mocks
summoner_response = {"id": "pepe"}
summoner_not_found_response = {
    "status": {"message": "Data not found - summoner not found", "status_code": 404}
}
invalid_api_key = {"status": {"message": "Forbidden", "status_code": 403}}


@pytest.mark.asyncio
async def test_get_summoner_by_name(test_app, respx_mock):
    respx_mock.get(
        "https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-name/stradivari96"
    ).mock(return_value=httpx.Response(204, json=summoner_response))
    response = await get_summoner_by_name("stradivari96", "euw1")
    assert response == summoner_response


@pytest.mark.asyncio
async def test_get_summoner_by_name_invalid_name(test_app, respx_mock):
    respx_mock.get(
        "https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-name/stradivari96"
    ).mock(return_value=httpx.Response(204, json=summoner_not_found_response))
    with pytest.raises(SummonerNotFoundException):
        await get_summoner_by_name("stradivari96", "euw1")


@pytest.mark.asyncio
async def test_get_summoner_by_name_invalid_key(test_app, respx_mock):
    respx_mock.get(
        "https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-name/stradivari96"
    ).mock(return_value=httpx.Response(204, json=invalid_api_key))
    with pytest.raises(InvalidAPIKeyException):
        await get_summoner_by_name("stradivari96", "euw1")
