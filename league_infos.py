from typing import List

import requests
from bs4 import BeautifulSoup


def get_league_urls(root: str) -> List[str]:
    response = requests.get(root)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    league_links = soup.find_all("a", class_="link list-item")
    valid_urls = [
        f"https://www.handball.net{link.get('href')}" for link in league_links
    ]
    return valid_urls


def get_game_urls(league_url: str) -> List[str]:
    response = requests.get(league_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return [
        f"https://www.handball.net{link.get('href')}"
        for link in soup.find_all("a", class_="link schedule-list-item")
    ]
