from app.infrastructure.db.database import async_session
from app.infrastructure.repositories.player_repo import PlayerRepository
from app.services.match_service import MatchService
from app.services.ranked_service import RankedEntriesService
from app.dependencies import riot_client


async def update_player_data_task(puuid: str) -> None:
    """Фоновая задача обновления данных игрока."""

    async with async_session() as db:
        player_repo = PlayerRepository(db)
        player = await player_repo.get_by_puuid(puuid)
        if not player:
            return

        ranked_service = RankedEntriesService(
            db=db,
            riot_client=riot_client,
        )

        match_service = MatchService(
            db=db,
            riot_client=riot_client,
        )

        await ranked_service.update_ranked_entries(player)
        await match_service.update_player_matches(puuid)
