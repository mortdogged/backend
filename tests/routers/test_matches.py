from unittest.mock import patch

from app.exceptions import SummonerNotFoundException

matches = ["1", "2", "3"]


async def summoner_not_found(name, platform):
    raise SummonerNotFoundException


async def mock_get_summoner_by_name(name, platform):
    return {"id": "pepe", "profileIconId": 1, "puuid": "sds"}


async def mock_get_matches(puuid, region):
    return matches


@patch("app.routers.matches.get_matches", mock_get_matches)
@patch("app.routers.matches.get_summoner_by_name", mock_get_summoner_by_name)
def test_list_matches(test_app):
    response = test_app.get("/matches/?platform=euw1&summoner_name=vivapy")
    assert response.status_code == 200
    assert response.json() == matches


@patch("app.routers.matches.get_summoner_by_name", summoner_not_found)
def test_list_matches_invalid_summoner_name(test_app):
    response = test_app.get("/matches/?platform=euw1&summoner_name=vivapy")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summoner not found"
