from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.database import get_db
from app.infrastructure.repositories.match_participant_repo import (
    MatchParticipantRepository,
)
from app.infrastructure.repositories.player_repo import PlayerRepository
from app.infrastructure.repositories.match_repo import GameMatchRepository
from app.services.client import RiotClient
from app.services.champion_stats import ChampionStatsService
from app.schemas import (
    ChampionStatsResponse,
    PlayerOut,
    MatchParticipantOut,
    GameMatchOut,
)
from app.dependencies import (
    get_riot_client,
    get_player_repo,
    get_match_participant_repo,
    get_match_repo,
)

router = APIRouter(prefix="/players", tags=["players"])


@router.get("/{game_name}/{tag_line}", response_model=PlayerOut)
async def get_player(
    game_name: str,
    tag_line: str,
    riot_client: RiotClient = Depends(get_riot_client),
    db: AsyncSession = Depends(get_db),
    player_repo: PlayerRepository = Depends(get_player_repo),
):
    account_data = await riot_client.get_account_by_riot_id(game_name, tag_line)

    if not account_data:
        raise HTTPException(status_code=404, detail="Player not found")

    summoner_data = await riot_client.get_summoner_by_puuid(account_data["puuid"])

    await player_repo.create_or_update_player(account_data, summoner_data)

    player = await player_repo.get_by_puuid_with_ranked(account_data["puuid"])

    return player


@router.get("/{puuid}/champions", response_model=ChampionStatsResponse)
async def get_champion_stats(
    puuid: str,
    db: AsyncSession = Depends(get_db),
    player_repo: PlayerRepository = Depends(get_player_repo),
):
    player = await player_repo.get_by_puuid(puuid)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    service = ChampionStatsService(db)
    stats = await service.champion_stats(player.id)

    return ChampionStatsResponse(player_id=player.id, champions=stats)


@router.get(
    "/players/{puuid}/matches_participants", response_model=List[MatchParticipantOut]
)
async def get_matches_participants(
    puuid: str,
    limit: int = 20,
    player_repo: PlayerRepository = Depends(get_player_repo),
    match_participant_repo: MatchParticipantRepository = Depends(
        get_match_participant_repo
    ),
):
    player = await player_repo.get_by_puuid(puuid)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    matches = await match_participant_repo.get_matches_by_player_id(player.id, limit)
    return matches


@router.get("/players/{puuid}/matches", response_model=List[GameMatchOut])
async def get_game_matches(
    puuid: str,
    limit: int = 20,
    player_repo: PlayerRepository = Depends(get_player_repo),
    match_repo: GameMatchRepository = Depends(get_match_repo),
):
    player = await player_repo.get_by_puuid(puuid)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    matches = await match_repo.get_matches_by_player_puuid(puuid, limit)
    if not matches:
        raise HTTPException(status_code=404, detail="Matches not found")
    return matches
