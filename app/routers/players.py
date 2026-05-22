from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.infrastructure.repositories.match_participant_repo import (
    MatchParticipantRepository,
)
from app.infrastructure.repositories.player_repo import PlayerRepository
from app.infrastructure.repositories.match_repo import GameMatchRepository
from app.services.player_service import PlayerService
from app.services.champion_stats import ChampionStatsService
from app.schemas import (
    ChampionStatsResponse,
    PlayerOut,
    MatchParticipantOut,
    GameMatchOut,
)
from app.dependencies import (
    get_player_repo,
    get_match_participant_repo,
    get_match_repo,
    get_player_service,
    get_champion_stats_service,
)
from app.exceptions import PlayerNotFoundError

router = APIRouter(prefix="/players", tags=["players"])


@router.post("/{game_name}/{tag_line}", response_model=PlayerOut)
async def create_player(
    game_name: str,
    tag_line: str,
    player_service: PlayerService = Depends(get_player_service),
):
    try:
        player = await player_service.create_player(game_name, tag_line)
    except PlayerNotFoundError:
        raise HTTPException(status_code=404, detail="Player not found")

    return PlayerOut.model_validate(player)


@router.get("/{puuid}", response_model=PlayerOut)
async def get_player_from_db(
    puuid: str,
    player_repo: PlayerRepository = Depends(get_player_repo),
):
    player = await player_repo.get_by_puuid_with_ranked(puuid)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    return PlayerOut.model_validate(player)


@router.get("/{puuid}/champions", response_model=ChampionStatsResponse)
async def get_champion_stats(
    puuid: str,
    champion_stats_service: ChampionStatsService = Depends(get_champion_stats_service),
    player_repo: PlayerRepository = Depends(get_player_repo),
):
    player = await player_repo.get_by_puuid(puuid)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    stats = await champion_stats_service.champion_stats(player.id)

    return ChampionStatsResponse(player_id=player.id, champions=stats)


@router.get("/{puuid}/matches_participants", response_model=List[MatchParticipantOut])
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
    return [MatchParticipantOut.model_validate(m) for m in matches]


@router.get("/{puuid}/matches", response_model=List[GameMatchOut])
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
    return [GameMatchOut.model_validate(m) for m in matches]
