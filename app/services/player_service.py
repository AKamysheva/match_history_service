from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.repositories.player_repo import PlayerRepository
from app.services.client import RiotClient
from app.exceptions import PlayerNotFoundError
from app.models.models import Player


class PlayerService:
    """Сервис работы с игроками."""

    def __init__(
        self, db: AsyncSession, riot_client: RiotClient, player_repo: PlayerRepository
    ) -> None:
        self.db = db
        self.riot_client = riot_client
        self.player_repo = player_repo

    async def create_player(self, game_name: str, tag_line: str) -> Player:
        account_data = await self.riot_client.get_account_by_riot_id(
            game_name, tag_line
        )

        if not account_data:
            raise PlayerNotFoundError("Player not found")

        summoner_data = await self.riot_client.get_summoner_by_puuid(
            account_data["puuid"]
        )

        player = await self.player_repo.create_or_update_player(
            account_data, summoner_data
        )
        await self.db.commit()

        return player
