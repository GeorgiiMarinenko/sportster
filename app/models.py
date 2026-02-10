from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Float,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, unique=True, index=True)          # Telegram ID
    username = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    rating = relationship("Rating", back_populates="user", uselist=False)
    matches_as_player1 = relationship(
        "Match",
        back_populates="player1",
        foreign_keys="Match.player1_id",
    )
    matches_as_player2 = relationship(
        "Match",
        back_populates="player2",
        foreign_keys="Match.player2_id",
    )


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    player1_id = Column(Integer, ForeignKey("users.id"))
    player2_id = Column(Integer, ForeignKey("users.id"))
    player1_score = Column(Integer)  # количество выигранных геймов
    player2_score = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    player1 = relationship("User", foreign_keys=[player1_id], back_populates="matches_as_player1")
    player2 = relationship("User", foreign_keys=[player2_id], back_populates="matches_as_player2")

    rating_changes = relationship("RatingHistory", back_populates="match")


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    current_rating = Column(Float, default=1000.0)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="rating")


class RatingHistory(Base):
    __tablename__ = "rating_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    match_id = Column(Integer, ForeignKey("matches.id"))
    old_rating = Column(Float)
    new_rating = Column(Float)
    delta = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    match = relationship("Match", back_populates="rating_changes")
