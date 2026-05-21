from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.database import get_db
from app.infrastructure.repositories.player_repo import PlayerRepository
from app.infrastructure.repositories.match_participant_repo import (
    MatchParticipantRepository,
)
from app.infrastructure.repositories.match_repo import GameMatchRepository
from app.services.client import RiotClient

riot_client = RiotClient()


def get_riot_client():
    return riot_client


def get_player_repo(db: AsyncSession = Depends(get_db)):
    player_repo = PlayerRepository(db)
    return player_repo


def get_match_participant_repo(db: AsyncSession = Depends(get_db)):
    match_participant_repository = MatchParticipantRepository(db)
    return match_participant_repository


def get_match_repo(db: AsyncSession = Depends(get_db)):
    match_repo = GameMatchRepository(db)
    return match_repo
