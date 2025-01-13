# FastAPI League Management API

This API allows users to manage and query data for **leagues**, **teams**, and **games**.



## Endpoints

| Method | Endpoint                        | Description              |
|--------|---------------------------------|--------------------------|
| GET    | `/`                             | Read Root               |
| GET    | `/leagues/`                     | Get All Leagues         |
| GET    | `/leagues/{league_id}`          | Get League              |
| GET    | `/teams/`                       | Get All Teams           |
| GET    | `/teams/{team_id}`              | Get Team                |
| GET    | `/games/`                       | Get All Games           |
| GET    | `/games/{game_id}`              | Get Game                |
| GET    | `/leagues/{league_id}/games`    | Get Games For League    |