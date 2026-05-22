from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.database import get_db
from app.infrastructure.repositories.player_repo import PlayerRepository
from app.infrastructure.repositories.match_participant_repo import (
    MatchParticipantRepository,
)
from app.infrastructure.repositories.match_repo import GameMatchRepository
from app.services.match_service import MatchService
from app.services.ranked_service import RankedEntriesService
from app.services.client import RiotClient
from app.services.player_service import PlayerService
from app.services.champion_stats import ChampionStatsService

riot_client = RiotClient()


def get_riot_client():
    return riot_client


def get_player_repo(db: AsyncSession = Depends(get_db)):
    player_repo = PlayerRepository(db)
    return player_repo


def get_match_participant_repo(db: AsyncSession = Depends(get_db)):
    match_participant_repository = MatchParticipantRepository(db)
    return match_participant_repository


def get_match_repo(db: AsyncSession = Depends(get_db)) -> GameMatchRepository:
    match_repo = GameMatchRepository(db)
    return match_repo


def get_player_service(
    db: AsyncSession = Depends(get_db),
    riot_client: RiotClient = Depends(get_riot_client),
    player_repo: PlayerRepository = Depends(get_player_repo),
) -> PlayerService:
    player_service = PlayerService(db, riot_client, player_repo)
    return player_service


def get_match_service(
    db: AsyncSession = Depends(get_db),
    riot_client: RiotClient = Depends(get_riot_client),
) -> MatchService:
    match_service = MatchService(db, riot_client)
    return match_service


def get_ranked_entries_service(
    db: AsyncSession = Depends(get_db),
    riot_client: RiotClient = Depends(get_riot_client),
) -> RankedEntriesService:
    ranked_service = RankedEntriesService(db, riot_client)
    return ranked_service


def get_champion_stats_service(
    db: AsyncSession = Depends(get_db),
) -> ChampionStatsService:
    champion_stats_service = ChampionStatsService(db)
    return champion_stats_service
