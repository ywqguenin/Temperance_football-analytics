from src.agent import execute_tools, ToolDecision
from src.data_loader import load_match_events


MATCH_ID = 3754296


def test_execute_shot_analysis():
    events = load_match_events(MATCH_ID)

    decision = ToolDecision(
        tools=["shot_analysis"],
        teams=["Arsenal", "Manchester City"],
        reason="Test shot analysis."
    )

    evidence = execute_tools(
        events,
        decision
    )

    assert evidence["shot_analysis"]["Arsenal"]["shots"] == 8
    assert evidence["shot_analysis"]["Manchester City"]["shots"] == 19

    assert evidence["shot_analysis"]["Arsenal"]["total_xg"] == 1.354
    assert evidence["shot_analysis"]["Manchester City"]["total_xg"] == 1.25


def test_execute_final_third_entries():
    events = load_match_events(MATCH_ID)

    decision = ToolDecision(
        tools=["final_third_entries"],
        teams=["Arsenal", "Manchester City"],
        reason="Test final third entries."
    )

    evidence = execute_tools(
        events,
        decision
    )

    assert evidence["final_third_entries"]["Arsenal"] == 29
    assert evidence["final_third_entries"]["Manchester City"] == 39


def test_execute_progressive_passes():
    events = load_match_events(MATCH_ID)

    decision = ToolDecision(
        tools=["progressive_passes"],
        teams=["Arsenal", "Manchester City"],
        reason="Test progressive passes."
    )

    evidence = execute_tools(
        events,
        decision
    )

    assert evidence["progressive_passes"]["Arsenal"] == 85
    assert evidence["progressive_passes"]["Manchester City"] == 123


def test_execute_team_summary():
    events = load_match_events(MATCH_ID)

    decision = ToolDecision(
        tools=["team_summary"],
        teams=["Arsenal", "Manchester City"],
        reason="Test team summary."
    )

    evidence = execute_tools(
        events,
        decision
    )

    arsenal = evidence["team_summary"]["Arsenal"]
    city = evidence["team_summary"]["Manchester City"]

    assert arsenal["shots"] == 8
    assert arsenal["total_xg"] == 1.354
    assert arsenal["final_third_entries"] == 29

    assert city["shots"] == 19
    assert city["total_xg"] == 1.25
    assert city["final_third_entries"] == 39
