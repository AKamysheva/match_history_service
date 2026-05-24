from datetime import datetime, UTC

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import GameMatch, MatchParticipant
from app.services.client import RiotClient


class MatchService:
    """Сервис работы с данными матчей из Riot API."""

    def __init__(self, db: AsyncSession, riot_client: RiotClient) -> None:
        self.db = db
        self.riot_client = riot_client

    async def update_player_matches(self, puuid: str) -> None:
        match_ids = await self.riot_client.get_match_ids(puuid)

        existing_matches = await self.db.execute(
            select(GameMatch.match_id).where(GameMatch.match_id.in_(match_ids))
        )
        existing_ids = set(existing_matches.scalars().all())
        new_match_ids = [m for m in match_ids if m not in existing_ids]

        for match_id in new_match_ids:
            data = await self.riot_client.get_match(match_id)

            if not data:
                continue

            info = data["info"]

            match = GameMatch(
                match_id=match_id,
                queue_id=info["queueId"],
                platform_id=info["platformId"],
                patch=".".join(info["gameVersion"].split(".")[:2]),
                start_time=datetime.fromtimestamp(
                    info["gameCreation"] / 1000,
                    tz=UTC,
                ),
                game_duration=info["gameDuration"],
                raw_json=data,
            )

            self.db.add(match)
            await self.db.flush()

            participants = []

            for p in info["participants"]:

                deaths = max(p["deaths"], 1)

                participant = MatchParticipant(
                    match_pk_id=match.id,
                    puuid=p["puuid"],
                    champion_id=p["championId"],
                    champion_name=p["championName"],
                    team_id=p["teamId"],
                    team_position=p.get("teamPosition"),
                    kills=p["kills"],
                    deaths=p["deaths"],
                    assists=p["assists"],
                    gold_earned=p["goldEarned"],
                    gold_spent=p["goldSpent"],
                    win=p["win"],
                    kda=round((p["kills"] + p["assists"]) / deaths, 2),
                    raw_json=p,
                )
                participants.append(participant)

            self.db.add_all(participants)

        await self.db.commit()
