import math
import pandas as pd


def _validate_columns(events, required_columns):
    missing = [
        column
        for column in required_columns
        if column not in events.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )


def _validate_team(events, team):
    _validate_columns(events, ["team"])

    available_teams = events["team"].dropna().unique()

    if team not in available_teams:
        raise ValueError(
            f"Team '{team}' not found. "
            f"Available teams: {list(available_teams)}"
        )


def get_team_shots(events, team):
    _validate_columns(
        events,
        ["type", "team", "shot_statsbomb_xg"]
    )
    _validate_team(events, team)

    return events[
        (events["type"] == "Shot") &
        (events["team"] == team)
    ].copy()


def get_team_passes(events, team):
    _validate_columns(
        events,
        ["type", "team", "pass_outcome"]
    )
    _validate_team(events, team)

    return events[
        (events["type"] == "Pass") &
        (events["team"] == team)
    ].copy()


def get_final_third_entries(events, team):

    _validate_columns(
        events,
        [
            "type",
            "team",
            "pass_outcome",
            "location",
            "pass_end_location"
        ]
    )

    _validate_team(events, team)

    passes = events[
        (events["type"] == "Pass") &
        (events["team"] == team) &
        (events["pass_outcome"].isna())
    ].copy()

    passes = passes[
        passes["location"].notna() &
        passes["pass_end_location"].notna()
    ].copy()

    passes["start_x"] = passes["location"].apply(lambda x: x[0])
    passes["end_x"] = passes["pass_end_location"].apply(lambda x: x[0])

    return passes[
        (passes["start_x"] < 80) &
        (passes["end_x"] >= 80)
    ].copy()


def get_progressive_passes(events, team, min_progress=10):

    _validate_columns(
        events,
        [
            "type",
            "team",
            "pass_outcome",
            "location",
            "pass_end_location"
        ]
    )

    _validate_team(events, team)

    passes = events[
        (events["type"] == "Pass") &
        (events["team"] == team) &
        (events["pass_outcome"].isna())
    ].copy()

    passes = passes[
        passes["location"].notna() &
        passes["pass_end_location"].notna()
    ].copy()

    def distance_to_goal(location):
        x, y = location
        goal_x, goal_y = 120, 40
        return math.sqrt((goal_x - x) ** 2 + (goal_y - y) ** 2)

    passes["start_goal_distance"] = passes["location"].apply(distance_to_goal)
    passes["end_goal_distance"] = passes["pass_end_location"].apply(
        distance_to_goal)

    passes["progress"] = (
        passes["start_goal_distance"] -
        passes["end_goal_distance"]
    )

    return passes[
        passes["progress"] >= min_progress
    ].copy()


def build_team_summary(events, team):
    shots = get_team_shots(events, team)
    passes = get_team_passes(events, team)
    entries = get_final_third_entries(events, team)
    progressive = get_progressive_passes(events, team)

    completed_passes = passes["pass_outcome"].isna().sum()

    return {
        "team": team,
        "shots": len(shots),
        "total_xg": float(
            round(shots["shot_statsbomb_xg"].sum(), 3)
        ),
        "average_xg_per_shot": (
            float(round(shots["shot_statsbomb_xg"].mean(), 3))
            if len(shots) > 0
            else 0.0
        ),
        "passes": len(passes),
        "completed_passes": int(completed_passes),
        "pass_completion_rate": (
            float(round(completed_passes / len(passes) * 100, 2))
            if len(passes) > 0
            else 0.0
        ),
        "final_third_entries": len(entries),
        "progressive_passes": len(progressive)
    }
