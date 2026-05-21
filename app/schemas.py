from datetime import datetime
from pydantic import BaseModel, ConfigDict


class RankedOut(BaseModel):
    queue_type: str
    tier: str
    rank: str
    league_points: int
    wins: int
    losses: int


class PlayerOut(BaseModel):
    id: int
    puuid: str
    game_name: str
    tag_line: str

    ranked: list[RankedOut] = []

    model_config = ConfigDict(extra="ignore", from_attributes=True)


class ChampionStatsItem(BaseModel):
    champion_name: str
    games: int
    avg_kda: float
    winrate: float


class ChampionStatsResponse(BaseModel):
    player_id: int
    champions: list[ChampionStatsItem]


class MatchParticipantOut(BaseModel):
    match_pk_id: int
    champion_name: str
    team_position: str
    kills: int
    deaths: int
    assists: int
    gold_earned: int
    gold_spent: int
    win: bool
    kda: float

    model_config = ConfigDict(extra="ignore", from_attributes=True)


class GameMatchOut(BaseModel):
    match_id: str
    queue_id: int
    platform_id: str
    patch: str
    start_time: datetime
    game_duration: int
    participants: list[MatchParticipantOut] = []

    model_config = ConfigDict(extra="ignore", from_attributes=True)
