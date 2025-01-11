# FastAPI League Management API

This API allows users to manage and query data for **leagues**, **teams**, and **games**.

## Table of Contents
- [FastAPI League Management API](#fastapi-league-management-api)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Endpoints](#endpoints)
    - [**Leagues**](#leagues)
      - [Responses:](#responses)

---

## Overview

The API includes the following features:
1. Manage **Leagues**, which contain multiple **Teams**.
2. Manage **Teams**, which belong to a specific **League** and participate in **Games**.
3. Manage **Games**, which include details such as goals, cards, and timestamps.

---

## Endpoints

### **Leagues**

| Method | Endpoint              | Description                                  |
|--------|-----------------------|----------------------------------------------|
| GET    | `/leagues/`           | Get all leagues (optionally include teams).  |
| GET    | `/leagues/{league_id}`| Get a specific league by `league_id`.        |

#### Responses:
- **`/leagues/`**
  ```json
  [
    {
      "league_id": "123",
      "league_name": "Premier League",
      "teams": [
        {
          "team_id": "550e8400-e29b-41d4-a716-446655440000",
          "team_name": "Team A",
          "league_id": "123"
        }
      ]
    }
  ]