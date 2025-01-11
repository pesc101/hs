import uuid

import pandas as pd
from sqlalchemy import Engine
from tqdm import tqdm

from game_infos import get_game_info
from init_db import create_db_engine
from league_infos import get_game_urls, get_league_urls


def fetch_game_data(
    league_urls: list[str], current_game_ids: list[str]
) -> pd.DataFrame:
    """
    Fetch game data for leagues while avoiding already processed games.
    Args:
        league_urls: list of league URLs.
        current_game_ids: list of already processed game IDs.
    Returns:
        DataFrame containing game data.
    """
    all_game_data = []
    for league_url in tqdm(
        league_urls, position=0, leave=False, desc="Processing Leagues"
    ):
        game_urls = get_game_urls(league_url)
        filtered_game_urls = [
            game_url
            for game_url in game_urls
            if game_url.split("/")[-1] not in current_game_ids
        ]
        game_data_list = []
        for game_url in tqdm(
            filtered_game_urls, position=1, leave=False, desc="Processing Games"
        ):
            game_info = get_game_info(game_url)
            if game_info.empty:
                break
            game_data_list.append(game_info)
        if game_data_list:
            all_game_data.append(pd.concat(game_data_list))
    return (
        pd.concat(all_game_data, ignore_index=True) if all_game_data else pd.DataFrame()
    )


def create_league_table(data: pd.DataFrame, engine: Engine) -> None:
    """Create the leagues table in the database."""
    data[["league_id", "league_name"]].drop_duplicates().to_sql(
        "leagues", engine, if_exists="append", index=False
    )


def create_team_table(data: pd.DataFrame, engine: Engine) -> None:
    """Create the teams table in the database."""
    data["team_id"] = data["team"].astype("category").cat.codes
    data["team_name"] = data["team"]
    data[["team_id", "team_name", "league_id"]].drop_duplicates().to_sql(
        "teams", engine, if_exists="append", index=False
    )


def update_game_table(data: pd.DataFrame, engine: Engine) -> None:
    """Update the game details table in the database."""
    data["record_id"] = data["game_id"].apply(lambda x: uuid.uuid4())
    data.drop(columns=["league_name", "team_name", "team"], inplace=True)
    data.to_sql("game_details", engine, if_exists="append", index=False)


def main() -> None:
    """Main function to process and store game data."""
    root_url = "https://www.handball.net/ligen?organization=Hamburg"
    engine = create_db_engine()
    league_urls = get_league_urls(root_url)
    current_status = pd.read_sql_table("game_details", engine)
    current_game_ids = current_status["game_id"].unique().tolist()

    game_data = fetch_game_data(league_urls, current_game_ids)
    if not game_data.empty:
        create_league_table(game_data, engine)
        create_team_table(game_data, engine)
        update_game_table(game_data, engine)


if __name__ == "__main__":
    main()
