from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from app.infrastructure.repositories.player_repo import PlayerRepository
from app.tasks import update_player_data_task
from app.dependencies import get_player_repo

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/players/{puuid}/update")
async def update_player_matches(
    puuid: str,
    background_tasks: BackgroundTasks,
    player_repo: PlayerRepository = Depends(get_player_repo),
) -> dict[str, str]:
    """Обновляет ranked entries и историю матчей игрока."""
    player = await player_repo.get_by_puuid(puuid)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    background_tasks.add_task(
        update_player_data_task,
        puuid,
    )

    return {"status": "player started updated in the background"}
