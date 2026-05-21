from app.infrastructure.repositories.player_repo import PlayerRepository
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.database import get_db
from app.services.match_service import MatchService
from app.services.ranked_service import RankedEntriesService
from app.dependencies import get_riot_client, get_player_repo

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/players/{puuid}/update")
async def update_player_matches(
    puuid: str,
    db: AsyncSession = Depends(get_db),
    riot_client=Depends(get_riot_client),
    player_repo: PlayerRepository = Depends(get_player_repo),
):
    player = await player_repo.get_by_puuid(puuid)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    match_service = MatchService(db, riot_client)
    ranked_service = RankedEntriesService(db, riot_client)

    await ranked_service.update_ranked_entries(player)
    await match_service.update_player_matches(player)

    return {"status": "player was updated"}
