import json
from unittest.mock import patch

import httpx
import pytest

from app.api.riot import get_matches, get_summoner_by_name
from app.exceptions import InvalidAPIKeyException, SummonerNotFoundException

# Mocks
profile_response = {
    "id": "pepe",
    "profile_icon_url": (
        "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data"
        "/global/default/v1/profile-icons/1.jpg"
    ),
}
summoner_response = {"id": "pepe", "profileIconId": 1, "status": {"status_code": 200}}
summoner_not_found_response = {
    "status": {"message": "Data not found - summoner not found", "status_code": 404}
}
invalid_api_key = {"status": {"message": "Forbidden", "status_code": 403}}


class FakeCacheFound:
    @staticmethod
    def get(_):
        return json.dumps(summoner_response)


class FakeCacheNotFound:
    @staticmethod
    def get(_):
        ...

    @staticmethod
    def set(x, y, ex):
        ...


@patch("app.api.riot.get_cache", FakeCacheFound)
async def test_get_summoner_by_name_cached(test_app):
    response = await get_summoner_by_name("stradivari96", "euw1")
    assert response == summoner_response


@patch("app.api.riot.get_cache", FakeCacheNotFound)
async def test_get_summoner_by_name(test_app, respx_mock):
    route = respx_mock.get(
        "https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-name/stradivari96"
    ).mock(return_value=httpx.Response(204, json=summoner_response))
    response = await get_summoner_by_name("stradivari96", "euw1")
    assert route.called
    assert response == summoner_response


@patch("app.api.riot.get_cache", FakeCacheNotFound)
async def test_get_summoner_by_name_invalid_name(test_app, respx_mock):
    respx_mock.get(
        "https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-name/stradivari96"
    ).mock(return_value=httpx.Response(204, json=summoner_not_found_response))
    with pytest.raises(SummonerNotFoundException):
        await get_summoner_by_name("stradivari96", "euw1")


@patch("app.api.riot.get_cache", FakeCacheNotFound)
async def test_get_summoner_by_name_invalid_key(test_app, respx_mock):
    respx_mock.get(
        "https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-name/stradivari96"
    ).mock(return_value=httpx.Response(204, json=invalid_api_key))
    with pytest.raises(InvalidAPIKeyException):
        await get_summoner_by_name("stradivari96", "euw1")


async def test_get_matches(test_app, respx_mock):
    respx_mock.get(
        "https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/24/ids"
    ).mock(return_value=httpx.Response(200, json=["1", "2", "3"]))

    response = await get_matches(24, "europe")
    assert response == ["1", "2", "3"]
