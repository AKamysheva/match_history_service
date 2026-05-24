from app.models.models import GameMatch
from sqlalchemy import func, Integer, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import MatchParticipant


class ChampionStatsService:
    """
    Сервис агрегированной статистики по чемпионам.
    Статистика считается только для SoloQ (queue_id = 420).
    """

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def champion_stats(self, puuid: str):
        stmt = (
            select(
                MatchParticipant.champion_name,
                func.count().label("games"),
                func.avg(MatchParticipant.kda).label("avg_kda"),
                func.avg(MatchParticipant.win.cast(Integer)).label("winrate"),
            )
            .join(
                GameMatch,
                GameMatch.id == MatchParticipant.match_pk_id,
            )
            .where(
                MatchParticipant.puuid == puuid,
                GameMatch.queue_id == 420,
            )
            .group_by(MatchParticipant.champion_name)
            .order_by(func.count().desc())
        )

        result = await self.db.execute(stmt)

        return [
            {
                "champion_name": row.champion_name,
                "games": row.games,
                "avg_kda": round(float(row.avg_kda or 0), 2),
                "winrate": float(row.winrate or 0),
            }
            for row in result.all()
        ]
