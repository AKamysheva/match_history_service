from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import MatchParticipant


class MatchParticipantRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_matches_by_puuid(
        self, puuid: str, limit: int = 20
    ) -> list[MatchParticipant]:
        stmt = (
            select(MatchParticipant)
            .where(MatchParticipant.puuid == puuid)
            .order_by(MatchParticipant.match_pk_id.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
