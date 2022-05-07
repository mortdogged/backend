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
        },
        {
            "queueType": "RANKED_TFT_TURBO",
            "ratedTier": "ORANGE",
            "ratedRating": "6464",
            "wins": 54,
            "losses": 147,
        },
        {
            "queueType": "RANKED_TFT_TURBO_DOUBLE",
            "ratedTier": "ORANGE",
            "ratedRating": "6777",
            "wins": 45,
            "losses": 89,
        },
    ]


matches = ["1", "2", "3"]


async def mock_get_matches(puuid, region):
    return matches


@pytest.mark.parametrize("username", ("stradivari96", "Stradivari 96"))
@patch("app.routers.profile.get_summoner_by_name", mock_get_summoner_by_name)
@patch("app.routers.profile.get_entries_for_summoner", mock_get_entries_for_summoner)
def test_profile(test_app, username):
    response = test_app.get(f"/profile/euw1/{username}")
    assert response.status_code == 200
    response_json = response.json()
    assert "name" in response_json
    assert len(response_json["other_queues"]) == 2


@patch("app.routers.profile.get_summoner_by_name", summoner_not_found)
def test_profile_invalid_summoner_name(test_app):
    response = test_app.get("/profile/euw1/stradivari96")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summoner not found"


def test_profile_not_homie(test_app):
    response = test_app.get("/profile/euw1/notahomie")
    assert response.status_code == 422


@patch("app.routers.profile.get_matches", mock_get_matches)
@patch("app.routers.profile.get_summoner_by_name", mock_get_summoner_by_name)
def test_list_matches(test_app):
    response = test_app.get("profile/euw1/vivapy/matches")
    assert response.status_code == 200
    assert set(response.json()) == set(matches)


@patch("app.routers.profile.get_summoner_by_name", summoner_not_found)
def test_list_matches_invalid_summoner_name(test_app):
    response = test_app.get("profile/euw1/vivapy/matches")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summoner not found"
