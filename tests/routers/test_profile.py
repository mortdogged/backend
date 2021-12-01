from unittest.mock import patch

import pytest

from app.exceptions import SummonerNotFoundException


# Mocks
async def summoner_not_found(name, platform):
    raise SummonerNotFoundException


async def mock_get_summoner_by_name(name, platform):
    return {"id": "pepe", "profileIconId": 1}


async def mock_get_entries_for_summoner(summoner_id, platform):
    return [
        {
            "name": "Stradivari96",
            "profileIconId": 4627,
            "summonerLevel": 164,
            "queueType": "RANKED_TFT",
            "tier": "MASTER",
            "rank": "I",
            "wins": 12,
            "losses": 90,
            "hotStreak": False,
        }
    ]


@pytest.mark.parametrize("username", ("stradivari96", "Stradivari 96"))
@patch("app.routers.profile.get_summoner_by_name", mock_get_summoner_by_name)
@patch("app.routers.profile.get_entries_for_summoner", mock_get_entries_for_summoner)
def test_profile(test_app, username):
    response = test_app.get(f"/profile/euw1/{username}")
    assert response.status_code == 200
    assert "name" in response.json()


@patch("app.routers.profile.get_summoner_by_name", summoner_not_found)
def test_profile_invalid_summoner_name(test_app):
    response = test_app.get("/profile/euw1/stradivari96")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summoner not found"


def test_profile_not_homie(test_app):
    response = test_app.get("/profile/euw1/notahomie")
    assert response.status_code == 422