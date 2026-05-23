from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Player, RankedEntry
from app.models.enums import Tier
from app.services.client import RiotClient


class RankedEntriesService:
    """Сервис загрузки ranked entries игрока."""

    def __init__(self, db: AsyncSession, riot_client: RiotClient) -> None:
        self.db = db
        self.riot_client = riot_client

    async def update_ranked_entries(self, player: Player) -> None:
        data = await self.riot_client.get_ranked_entries(player.puuid)

        if not data:
            return

        for entry in data:
            insert_stmt = insert(RankedEntry).values(
                player_id=player.id,
                queue_type=entry["queueType"],
                tier=Tier(entry["tier"]),
                rank=entry["rank"],
                league_points=entry["leaguePoints"],
                wins=entry["wins"],
                losses=entry["losses"],
            )

            do_update_stmt = insert_stmt.on_conflict_do_update(
                index_elements=["player_id", "queue_type"],
                set_={
                    "tier": Tier(entry["tier"]),
                    "rank": entry["rank"],
                    "league_points": entry["leaguePoints"],
                    "wins": entry["wins"],
                    "losses": entry["losses"],
                },
            )
            await self.db.execute(do_update_stmt)

        await self.db.commit()
