from app.infrastructure.repositories.player_repo import PlayerRepository
from fastapi import APIRouter, Depends, HTTPException
from app.services.match_service import MatchService
from app.services.ranked_service import RankedEntriesService
from app.dependencies import (
    get_player_repo,
    get_match_service,
    get_ranked_entries_service,
)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/players/{puuid}/update")
async def update_player_matches(
    puuid: str,
    match_service: MatchService = Depends(get_match_service),
    ranked_service: RankedEntriesService = Depends(get_ranked_entries_service),
    player_repo: PlayerRepository = Depends(get_player_repo),
):
    player = await player_repo.get_by_puuid(puuid)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    await ranked_service.update_ranked_entries(player)
    await match_service.update_player_matches(player)

    return {"status": "player was updated"}
