from pydantic import BaseModel, HttpUrl


# https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types
class Homie(str):
    homies = ["stradivari96", "frenfrenburger", "vivapy"]

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

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


class ProfileResponseSchema(BaseModel):
    name: str
    profile_icon_url: HttpUrl
    summonerLevel: int
    leaguePoints: int = None

    # TODO: Literals?
    tier: str = None
    rank: str = None

    wins: int = None
    losses: int = None
