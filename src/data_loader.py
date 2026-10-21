from pathlib import Path

import pandas as pd
from statsbombpy import sb


def load_matches(
    competition_id: int,
    season_id: int
):
    data_path = Path(
        f"data/matches_{competition_id}_{season_id}.pkl"
    )

    if data_path.exists():
        print("Loading match list from local cache...")
        return pd.read_pickle(data_path)

    print("Match list not found locally. Downloading from StatsBomb...")

    matches = sb.matches(
        competition_id=competition_id,
        season_id=season_id
    )

    data_path.parent.mkdir(exist_ok=True)

    matches.to_pickle(data_path)

    print("Match list saved locally.")

    return matches


def get_match_options(matches):
    return matches[
        [
            "match_id",
            "match_date",
            "home_team",
            "away_team"
        ]
    ].copy()


def load_match_events(match_id: int):
    data_path = Path(
        f"data/match_{match_id}_events.pkl"
    )

    if data_path.exists():
        print("Loading match data from local cache...")
        return pd.read_pickle(data_path)

    print("Local data not found. Downloading from StatsBomb...")

    events = sb.events(
        match_id=match_id
    )

    data_path.parent.mkdir(exist_ok=True)

    events.to_pickle(data_path)

    print("Match data saved locally.")

    return events
