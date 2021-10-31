from pydantic import BaseModel


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
