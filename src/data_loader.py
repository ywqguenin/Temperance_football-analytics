from pathlib import Path

import pandas as pd
from statsbombpy import sb


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
