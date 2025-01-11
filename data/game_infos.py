import locale
import re
from datetime import datetime
from typing import List, Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Regular expressions for card detection
YELLOW_REGEX = re.compile(r"icon_event_yellow\.svg")
RED_REGEX = re.compile(r"icon_event_red\.svg")


def get_soup(url: str) -> BeautifulSoup:
    """Fetches and parses HTML from a URL."""
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    return BeautifulSoup(response.text, "html.parser")


def extract_team_names(table: BeautifulSoup) -> List[str]:
    """Extracts team names from the table."""
    return [header.text.strip() for header in table.find_all("h3", class_="headline")]


def extract_league_name(soup: BeautifulSoup) -> str:
    """Extracts league name from the soup."""
    return soup.find(
        "h1", class_="truncate headline text-xl font-semibold"
    ).text.strip()


def determine_card(content: str) -> Optional[str]:
    """Determines the card type from SVG content."""
    if YELLOW_REGEX.search(content):
        return "yellow"
    if RED_REGEX.search(content):
        return "red"
    return None


def extract_team_data(table: BeautifulSoup) -> pd.DataFrame:
    """Extracts team player data from a table."""
    team_data = []
    rows = table.find_all("tr")[1:]  # Skip header row
    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 0:
            player_number = cols[0].text.strip().rstrip(".")
            player_name = cols[1].text.strip()
            if len(cols) > 2:
                goals = cols[2].text.strip() or "0"
            else:
                goals = "0"
            if len(cols) > 3:
                two_min_penalties = cols[3].text.strip() or "0"
            else:
                two_min_penalties = "0"
            if len(cols) > 4:
                cards = determine_card(str(cols[4]))
            else:
                cards = None
            team_data.append(
                {
                    "number": player_number,
                    "name": player_name,
                    "goals": goals,
                    "two_min": two_min_penalties,
                    "card": cards,
                }
            )
    return pd.DataFrame(team_data)


def extract_scoreboard_data(scoreboard: BeautifulSoup) -> List[dict]:
    """Extracts teams and their scores from the scoreboard."""
    teams_scores = []
    rows = scoreboard.find_all("tr")
    for row in rows:
        team_name = row.find("td", class_="tik3-scoreboard-team")
        score = row.find("td", class_="tik3-scoreboard-score")
        if team_name and score:
            team_name_text = team_name.find_all("div")[2].text.strip()
            score_text = score.find("div").text.strip()
            teams_scores.append({"team": team_name_text, "score": score_text})
    return teams_scores


def extract_game_date(soup: BeautifulSoup) -> datetime:
    """Extracts game date, time, and affiliations."""
    date = soup.find("span", class_="tik3-event-item-meta-timestamp-date")
    time = soup.find("span", class_="tik3-event-item-meta-timestamp-time")
    date_text = date.get_text(strip=True) if date else None
    time_text = time.get_text(strip=True) if time else None
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")

    return (
        datetime.strptime(f"{date_text} {time_text}", "%A, %d.%m.%Y %H:%M")
        if date_text and time_text
        else None
    )


def get_game_info(url: str) -> pd.DataFrame:
    """Extracts game info and returns it as a DataFrame."""
    soup = get_soup(url)
    league_name = extract_league_name(soup)

    # Extract teams and players
    table = soup.find("div", {"id": "aufstellung"})

    game_date = extract_game_date(soup)
    team_names = extract_team_names(table)
    team_tables = table.find_all("table")
    if len(team_tables) < 2:
        return pd.DataFrame()

    team_1_data = extract_team_data(team_tables[0])
    team_2_data = extract_team_data(team_tables[1])
    team_1_data["team"] = team_names[0]
    team_2_data["team"] = team_names[1]
    game_data = pd.concat([team_1_data, team_2_data], axis=0)
    game_data["goals"] = game_data["goals"].astype(int)
    game_data["team"] = game_data["team"].astype(str)
    game_data["two_min"] = game_data["two_min"].astype(int)
    game_data["card"] = game_data["card"].astype(str)
    game_data["date"] = game_date
    game_data["game_id"] = url.split("/")[-1]
    game_data["league_id"] = url.split("/")[-3]
    game_data["league_name"] = league_name

    return game_data
