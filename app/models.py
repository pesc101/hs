from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .db import engine

Base = declarative_base()


class League(Base):
    __tablename__ = "leagues"

    league_id = Column(String, primary_key=True, index=True)
    league_name = Column(String)

    teams = relationship("Team", back_populates="league")


class Team(Base):
    __tablename__ = "teams"

    team_id = Column(String, primary_key=True, index=True)
    team_name = Column(String)
    league_id = Column(String, ForeignKey("leagues.league_id"))

    league = relationship("League", back_populates="teams")
    games = relationship("GameDetails", back_populates="team")


class GameDetails(Base):
    __tablename__ = "game_details"

    record_id = Column(String, primary_key=True, index=True)
    game_id = Column(String)
    league_id = Column(String, ForeignKey("leagues.league_id"))
    number = Column(String)
    name = Column(String)
    goals = Column(Integer)
    two_min = Column(Integer)
    card = Column(String)
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.team_id"))
    date = Column(DateTime)

    # Relationships
    league = relationship("League")
    team = relationship("Team", back_populates="games")


Base.metadata.create_all(bind=engine)
