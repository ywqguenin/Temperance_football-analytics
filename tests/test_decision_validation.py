
import pandas as pd
from unittest.mock import patch
import pytest

from src.agent import ToolDecision, validate_decision


AVAILABLE_TEAMS = ["Crystal Palace", "Everton"]


def test_valid_decision():
    decision = ToolDecision(
        tools=["shot_analysis"],
        teams=["Crystal Palace", "Everton"],
        reason="Compare shooting performance."
    )

    validate_decision(decision, AVAILABLE_TEAMS)


def test_rejects_unknown_team():
    decision = ToolDecision(
        tools=["shot_analysis"],
        teams=["Arsenal"],
        reason="Test invalid team."
    )

    with pytest.raises(ValueError, match="Invalid team selection"):
        validate_decision(decision, AVAILABLE_TEAMS)


def test_rejects_empty_tools():
    decision = ToolDecision(
        tools=[],
        teams=["Crystal Palace"],
        reason="Test empty tools."
    )

    with pytest.raises(ValueError, match="no analytical tools"):
        validate_decision(decision, AVAILABLE_TEAMS)


def test_rejects_empty_teams():
    decision = ToolDecision(
        tools=["shot_analysis"],
        teams=[],
        reason="Test empty teams."
    )

    with pytest.raises(ValueError, match="no teams selected"):
        validate_decision(decision, AVAILABLE_TEAMS)


def test_rejects_duplicate_teams():
    decision = ToolDecision(
        tools=["shot_analysis"],
        teams=["Everton", "Everton"],
        reason="Test duplicate teams."
    )

    with pytest.raises(ValueError, match="duplicate teams"):
        validate_decision(decision, AVAILABLE_TEAMS)


def test_run_agent_rejects_empty_answer():
    events = pd.DataFrame({
        "team": ["Team A", "Team B"]
    })

    valid_decision = ToolDecision(
        tools=["shot_analysis"],
        teams=["Team A", "Team B"],
        reason="Test decision."
    )

    with (
        patch("src.agent.select_tools", return_value=valid_decision),
        patch("src.agent.execute_tools", return_value={"shot_analysis": {}}),
        patch("src.agent.generate_answer", return_value="   "),
        pytest.raises(ValueError, match="empty or invalid answer")
    ):
        from src.agent import run_agent
        run_agent(events, "Compare the teams.")
