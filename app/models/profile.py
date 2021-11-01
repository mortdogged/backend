from pydantic import BaseModel


# https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types
class Homie(str):
    homies = ["stradivari96", "frenfrenburger"]

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
    profileIconId: int
    summonerLevel: int

    # TODO: Literals?
    tier: str
    rank: str

    wins: int
    losses: int
    hotStreak: bool
