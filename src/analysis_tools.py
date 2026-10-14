from src.analysis_tools import build_team_summary
import math
import pandas as pd


def get_team_shots(events, team):
    return events[
        (events["type"] == "Shot") &
        (events["team"] == team)
    ].copy()


def get_team_passes(events, team):
    return events[
        (events["type"] == "Pass") &
        (events["team"] == team)
    ].copy()


def get_final_third_entries(events, team):
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
        "total_xg": round(shots["shot_statsbomb_xg"].sum(), 3),
        "average_xg_per_shot": round(
            shots["shot_statsbomb_xg"].mean(), 3
        ),
        "passes": len(passes),
        "completed_passes": int(completed_passes),
        "pass_completion_rate": round(
            completed_passes / len(passes) * 100, 2
        ),
        "final_third_entries": len(entries),
        "progressive_passes": len(progressive)
    }
