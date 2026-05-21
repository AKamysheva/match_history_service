from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import MatchParticipant


class ChampionStatsService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def champion_stats(
        self,
        player_id: int,
    ):

        stmt = (
            select(
                MatchParticipant.champion_name,
                func.count().label("games"),
                func.avg(MatchParticipant.kda).label("avg_kda"),
                func.avg(MatchParticipant.win.cast(int)).label("winrate"),
            )
            .where(MatchParticipant.player_id == player_id)
            .group_by(MatchParticipant.champion_name)
            .order_by(func.count().desc())
        )

        result = await self.db.execute(stmt)

        return [
            {
                "champion_name": row.champion_name,
                "games": row.games,
                "avg_kda": float(row.avg_kda or 0),
                "winrate": float(row.winrate or 0),
            }
            for row in result.all()
        ]
