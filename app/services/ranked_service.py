from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Player, RankedEntry
from app.models.enums import Tier
from app.services.client import RiotClient


class RankedEntriesService:
    def __init__(self, db: AsyncSession, riot_client: RiotClient) -> None:
        self.db = db
        self.riot_client = riot_client

    async def update_ranked_entries(self, player: Player) -> None:
        data = await self.riot_client.get_ranked_entries(player.puuid)
        await self.db.execute(
            delete(RankedEntry).where(RankedEntry.player_id == player.id)
        )

        if not data:
            await self.db.commit()
            return

        for entry in data:
            self.db.add(
                RankedEntry(
                    player_id=player.id,
                    queue_type=entry["queueType"],
                    tier=Tier(entry["tier"]),
                    rank=entry["rank"],
                    league_points=entry["leaguePoints"],
                    wins=entry["wins"],
                    losses=entry["losses"],
                )
            )

        await self.db.commit()
