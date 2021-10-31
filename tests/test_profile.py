from app.exceptions import SummonerNotFoundException


def test_profile(test_app, monkeypatch):
    monkeypatch.setattr(
        "app.api.profile.get_summoner_by_name", mock_get_summoner_by_name
    )
    monkeypatch.setattr(
        "app.api.profile.get_entries_for_summoner", mock_get_entries_for_summoner
    )
    response = test_app.get("/profile/euw1/stradivari96")
    assert response.status_code == 200
    assert "name" in response.json()


def test_profile_invalid_summoner_name(test_app, monkeypatch):
    monkeypatch.setattr("app.api.profile.get_summoner_by_name", summoner_not_found)
    response = test_app.get("/profile/euw1/riotstradivari")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summoner not found"


# Mocks
async def summoner_not_found(name, platform):
    raise SummonerNotFoundException


async def mock_get_summoner_by_name(name, platform):
    return {"id": "pepe"}


async def mock_get_entries_for_summoner(summoner_id, platform):
    return [
        {
            "name": "Stradivari96",
            "profileIconId": 4627,
            "summonerLevel": 164,
            "tier": "MASTER",
            "rank": "I",
            "wins": 12,
            "losses": 90,
            "hotStreak": False,
        }
    ]
