from typing import List

from pydantic import BaseModel, HttpUrl


# https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types
class Homie(str):
    homies = ["stradivari96", "frenfrenburger", "vivapy", "raconma"]

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(enum=cls.homies)

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("string required")
        v = v.replace(" ", "").lower()
        if v not in cls.homies:
            raise ValueError("invalid summoner name")
        return cls(v)

    def __repr__(self):
        return f"Homie({super().__repr__()})"


class Queues(BaseModel):
    queueType: str
    ratedTier: str
    ratedRating: str
    ratedRating: str
    wins: int
    losses: int


class ProfileResponseSchema(BaseModel):
    name: str
    profile_icon_url: HttpUrl
    summonerLevel: int
    leaguePoints: int = None
    other_queues: List[Queues]

    # TODO: Literals?
    tier: str = None
    rank: str = None

    wins: int = None
    losses: int = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Stradivari96",
                "profile_icon_url": "https://raw.communitydragon.org/latest/plugins/"
                "rcp-be-lol-game-data/global/default/v1/profile-icons/4627.jpg",
                "summonerLevel": 165,
                "leaguePoints": 20,
                "tier": "PLATINUM",
                "rank": "IV",
                "wins": 9,
                "losses": 49,
            }
        }
