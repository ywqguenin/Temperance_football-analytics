import pandas as pd
import pytest

from src.analysis_tools import build_team_summary


def test_zero_shots():
    events = pd.DataFrame([
        {
            "type": "Pass",
            "team": "Team A",
            "pass_outcome": None,
            "location": [30, 40],
            "pass_end_location": [50, 40],
            "shot_statsbomb_xg": None,
        }
    ])

    result = build_team_summary(events, "Team A")

    assert result["shots"] == 0
    assert result["total_xg"] == 0.0
    assert result["average_xg_per_shot"] == 0.0


def test_zero_passes():
    events = pd.DataFrame([
        {
            "type": "Shot",
            "team": "Team B",
            "pass_outcome": None,
            "location": [100, 40],
            "pass_end_location": None,
            "shot_statsbomb_xg": 0.25,
        }
    ])

    result = build_team_summary(events, "Team B")

    assert result["passes"] == 0
    assert result["completed_passes"] == 0
    assert result["pass_completion_rate"] == 0.0


def test_invalid_team():
    events = pd.DataFrame([
        {
            "type": "Pass",
            "team": "Team A",
            "pass_outcome": None,
            "location": [30, 40],
            "pass_end_location": [50, 40],
            "shot_statsbomb_xg": None,
        }
    ])

    with pytest.raises(ValueError, match="Team 'Unknown Team' not found"):
        build_team_summary(events, "Unknown Team")


def test_missing_required_column():
    events = pd.DataFrame([
        {
            "type": "Pass",
            "team": "Team C",
        }
    ])

    with pytest.raises(ValueError, match="Missing required columns"):
        build_team_summary(events, "Team C")
