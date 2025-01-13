import uuid
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .db import SessionLocal
from .models import GameDetails, League, Team
from .py_models import GameDetailsBase, LeagueBase, LeagueWithTeams, TeamBase

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8080"],  # Allow the Vue app (localhost:8080)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/leagues/", response_model=list[LeagueWithTeams])
def get_all_leagues(include_teams: bool = False, db: Session = Depends(get_db)):
    leagues = db.query(League).all()
    if not leagues:
        raise HTTPException(status_code=404, detail="No leagues found")
    if include_teams:
        return leagues
    return [LeagueBase(**league.__dict__) for league in leagues]


@app.get("/leagues/{league_id}", response_model=LeagueWithTeams)
def get_league(league_id: str, db: Session = Depends(get_db)):
    league = db.query(League).filter(League.league_id == str(league_id)).first()
    if not league:
        raise HTTPException(status_code=404, detail="League not found")
    return league


@app.get("/teams/", response_model=list[TeamBase])
def get_all_teams(league_id: Optional[str] = None, db: Session = Depends(get_db)):
    if league_id:
        teams = db.query(Team).filter(Team.league_id == league_id).all()
    else:
        teams = db.query(Team).all()
    if not teams:
        raise HTTPException(status_code=404, detail="No teams found")
    return teams


@app.get("/teams/{team_id}", response_model=list[TeamBase])
def get_team(team_id: str, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.team_id == str(team_id))
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@app.get("/games/", response_model=list[GameDetailsBase])
def get_all_games(
    league_id: Optional[str] = None,
    team_id: Optional[uuid.UUID] = None,
    db: Session = Depends(get_db),
):
    query = db.query(GameDetails)
    if league_id:
        query = query.filter(GameDetails.league_id == league_id)
    if team_id:
        query = query.filter(GameDetails.team_id == team_id)
    games = query.all()
    if not games:
        raise HTTPException(status_code=404, detail="No games found")
    return games


@app.get("/games/{game_id}", response_model=list[GameDetailsBase])
def get_game(game_id: str, db: Session = Depends(get_db)):
    game = db.query(GameDetails).filter(GameDetails.game_id == game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@app.get("/leagues/{league_id}/games", response_model=list[GameDetailsBase])
def get_games_for_league(league_id: str, db: Session = Depends(get_db)):
    games = db.query(GameDetails).filter(GameDetails.league_id == league_id).all()
    if not games:
        raise HTTPException(status_code=404, detail="No games found for this league")
    return games
