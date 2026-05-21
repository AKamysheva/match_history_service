from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import GameMatch
from app.models.models import Player
from app.models.models import MatchParticipant


class GameMatchRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_matches_by_player_puuid(
        self, puuid: str, limit: int = 20
    ) -> list[GameMatch]:
        stmt = (
            select(GameMatch)
            .join(MatchParticipant, MatchParticipant.match_pk_id == GameMatch.id)
            .join(Player, Player.id == MatchParticipant.player_id)
            .where(Player.puuid == puuid)
            .options(selectinload(GameMatch.participants))
            .order_by(GameMatch.start_time.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
