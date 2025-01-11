from datetime import datetime

from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GameDetailsBase(BaseModel):
    record_id: str
    game_id: str
    league_id: str
    number: int
    name: str
    goals: int
    two_min: int
    card: str | None
    team_id: str
    date: datetime

    class Config:
        orm_mode = True


class TeamBase(BaseModel):
    team_id: str
    team_name: str
    league_id: str

    class Config:
        orm_mode = True


class TeamWithGames(TeamBase):
    games: list[GameDetailsBase] = []


class LeagueBase(BaseModel):
    league_id: str
    league_name: str

    class Config:
        orm_mode = True


class LeagueWithTeams(LeagueBase):
    teams: list[TeamBase] = []
