from src.data_loader import (
    load_matches,
    get_match_options,
)


competition_id = 2
season_id = 27

matches = load_matches(
    competition_id,
    season_id
)

options = get_match_options(matches)

print(
    options.head(10).to_string(index=False)
)
