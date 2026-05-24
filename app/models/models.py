from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    Index,
    Integer,
    JSON,
    ForeignKey,
    Float,
    String,
    UniqueConstraint,
)
from datetime import datetime
from app.infrastructure.db.database import Base
from app.models.enums import Tier


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    puuid: Mapped[str] = mapped_column(String(78), unique=True, index=True)
    game_name: Mapped[str] = mapped_column(String, nullable=False)
    tag_line: Mapped[str] = mapped_column(String, nullable=False)
    region: Mapped[str] = mapped_column(String(10))
    profile_json: Mapped[dict | None] = mapped_column(
        JSON, nullable=True
    )  # summoner = player`s account LoL

    ranked_entries: Mapped[list["RankedEntry"]] = relationship(
        back_populates="player", cascade="all, delete-orphan", lazy="selectin"
    )

    __table_args__ = (Index("ix_players_game_name_tag", "game_name", "tag_line"),)


class RankedEntry(Base):
    __tablename__ = "ranked_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.id", ondelete="CASCADE")
    )
    queue_type: Mapped[str] = mapped_column(String)
    tier: Mapped[str] = mapped_column(Enum(Tier))  # Ранг
    rank: Mapped[str] = mapped_column(String)  # The player's division within a tier.
    league_points: Mapped[int] = mapped_column(Integer)
    wins: Mapped[int] = mapped_column(Integer)
    losses: Mapped[int] = mapped_column(Integer)

    player: Mapped["Player"] = relationship(back_populates="ranked_entries")

    __table_args__ = (
        UniqueConstraint("player_id", "queue_type", name="uq_player_queue"),
    )


class GameMatch(Base):
    __tablename__ = "game_matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    match_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    queue_id: Mapped[int] = mapped_column(Integer)
    platform_id: Mapped[str] = mapped_column(String)
    patch: Mapped[str] = mapped_column(String)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    game_duration: Mapped[int] = mapped_column(Integer)
    raw_json: Mapped[dict] = mapped_column(JSON)

    participants: Mapped[list["MatchParticipant"]] = relationship(
        back_populates="match", cascade="all, delete-orphan", lazy="selectin"
    )


class MatchParticipant(Base):
    __tablename__ = "match_participants"

    id: Mapped[int] = mapped_column(primary_key=True)
    match_pk_id: Mapped[int] = mapped_column(
        ForeignKey("game_matches.id", ondelete="CASCADE"), nullable=True
    )
    puuid: Mapped[str] = mapped_column(String(78), index=True)
    champion_id: Mapped[int] = mapped_column(Integer)
    champion_name: Mapped[str] = mapped_column(String)
    team_id: Mapped[int] = mapped_column(Integer)
    team_position: Mapped[str | None] = mapped_column(String)

    kills: Mapped[int] = mapped_column(Integer)
    deaths: Mapped[int] = mapped_column(Integer)
    assists: Mapped[int] = mapped_column(
        Integer
    )  # содействия (помощь в убийстве игроку противника)

    gold_earned: Mapped[int] = mapped_column(Integer)
    gold_spent: Mapped[int] = mapped_column(Integer)
    win: Mapped[bool] = mapped_column(Boolean)

    kda: Mapped[float] = mapped_column(Float)  # эффективность игрока в матче

    raw_json: Mapped[dict] = mapped_column(JSON)

    match: Mapped["GameMatch"] = relationship(back_populates="participants")

    __table_args__ = (
        UniqueConstraint(
            "match_pk_id",
            "puuid",
            name="uq_match_player",
        ),
    )
