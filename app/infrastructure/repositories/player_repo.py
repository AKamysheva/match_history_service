from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Player


class PlayerRepository:

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_puuid(self, puuid: str) -> Player | None:
        stmt = select(Player).where(Player.puuid == puuid)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_puuid_with_ranked(self, puuid: str) -> Player | None:
        stmt = (
            select(Player)
            .options(selectinload(Player.ranked_entries))
            .where(Player.puuid == puuid)
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_or_update_player(
        self, account_data: dict, summonner_data: dict
    ) -> None:
        player = await self.get_by_puuid(account_data["puuid"])

        if player:
            player.game_name = account_data["gameName"]
            player.tag_line = account_data["tagLine"]
            player.profile_json = summonner_data
        else:
            player = Player(
                puuid=account_data["puuid"],
                game_name=account_data["gameName"],
                tag_line=account_data["tagLine"],
                region="EUW",
                profile_json=summonner_data,
            )
            self.db.add(player)

        await self.db.commit()

        return player
