
import pandas as pd

from src.agent import execute_tools, ToolDecision


def make_test_events():
    """Create deterministic event data for testing the agent."""

    return pd.DataFrame([
        # Team A: two shots and two passes
        {
            "type": "Shot",
            "team": "Team A",
            "shot_statsbomb_xg": 0.4,
            "pass_outcome": None,
            "location": [80, 40],
            "pass_end_location": [100, 40],
        },
        {
            "type": "Shot",
            "team": "Team A",
            "shot_statsbomb_xg": 0.2,
            "pass_outcome": None,
            "location": [90, 30],
            "pass_end_location": [100, 40],
        },
        {
            "type": "Pass",
            "team": "Team A",
            "shot_statsbomb_xg": None,
            "pass_outcome": None,
            "location": [60, 40],
            "pass_end_location": [90, 40],
        },
        {
            "type": "Pass",
            "team": "Team A",
            "shot_statsbomb_xg": None,
            "pass_outcome": "Incomplete",
            "location": [50, 30],
            "pass_end_location": [55, 30],
        },

        # Team B: one shot and one completed pass
        {
            "type": "Shot",
            "team": "Team B",
            "shot_statsbomb_xg": 0.1,
            "pass_outcome": None,
            "location": [100, 40],
            "pass_end_location": [110, 40],
        },
        {
            "type": "Pass",
            "team": "Team B",
            "shot_statsbomb_xg": None,
            "pass_outcome": None,
            "location": [50, 40],
            "pass_end_location": [65, 40],
        },
    ])


def make_decision(tool):
    return ToolDecision(
        tools=[tool],
        teams=["Team A", "Team B"],
        reason="Unit test."
    )


def test_execute_shot_analysis():
    events = make_test_events()

    evidence = execute_tools(
        events,
        make_decision("shot_analysis")
    )

    assert set(evidence["shot_analysis"]) == {"Team A", "Team B"}

    assert evidence["shot_analysis"]["Team A"]["shots"] == 2
    assert evidence["shot_analysis"]["Team A"]["total_xg"] == 0.6
    assert evidence["shot_analysis"]["Team B"]["shots"] == 1
    assert evidence["shot_analysis"]["Team B"]["total_xg"] == 0.1


def test_execute_final_third_entries():
    events = make_test_events()

    evidence = execute_tools(
        events,
        make_decision("final_third_entries")
    )

    assert evidence["final_third_entries"]["Team A"] == 1
    assert evidence["final_third_entries"]["Team B"] == 0


def test_execute_progressive_passes():
    events = make_test_events()

    evidence = execute_tools(
        events,
        make_decision("progressive_passes")
    )

    assert evidence["progressive_passes"]["Team A"] == 1
    assert evidence["progressive_passes"]["Team B"] == 1


def test_execute_team_summary():
    events = make_test_events()

    evidence = execute_tools(
        events,
        make_decision("team_summary")
    )

    team_a = evidence["team_summary"]["Team A"]
    team_b = evidence["team_summary"]["Team B"]

    assert team_a["shots"] == 2
    assert team_a["total_xg"] == 0.6
    assert team_a["passes"] == 2
    assert team_a["completed_passes"] == 1
    assert team_a["pass_completion_rate"] == 50.0
    assert team_a["final_third_entries"] == 1
    assert team_a["progressive_passes"] == 1

    assert team_b["shots"] == 1
    assert team_b["total_xg"] == 0.1
    assert team_b["passes"] == 1
    assert team_b["completed_passes"] == 1
    assert team_b["pass_completion_rate"] == 100.0
    assert team_b["final_third_entries"] == 0
    assert team_b["progressive_passes"] == 1
