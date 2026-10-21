
import json
from types import SimpleNamespace

from src.agent import generate_answer


def fake_response(content):
    """Build a mock response with the same shape as Ollama's response."""
    return SimpleNamespace(
        message=SimpleNamespace(content=content)
    )


def test_generate_answer_returns_model_response(monkeypatch):
    """The function should return the generated answer without extra spaces."""
    expected_answer = (
        "Crystal Palace created better chances "
        "with higher total xG."
    )

    def fake_chat(**kwargs):
        return fake_response(f"  {expected_answer}  ")

    monkeypatch.setattr("src.agent.chat", fake_chat)

    answer = generate_answer(
        "Which team created better shooting chances?",
        {
            "shot_analysis": {
                "Crystal Palace": {
                    "shots": 20,
                    "total_xg": 2.665,
                    "average_xg_per_shot": 0.133,
                },
                "Everton": {
                    "shots": 9,
                    "total_xg": 0.592,
                    "average_xg_per_shot": 0.066,
                },
            }
        },
    )

    assert answer == expected_answer


def test_generate_answer_uses_expected_model_and_settings(monkeypatch):
    """The function should use the configured local model and temperature."""
    captured = {}

    def fake_chat(**kwargs):
        captured.update(kwargs)
        return fake_response("A test answer.")

    monkeypatch.setattr("src.agent.chat", fake_chat)

    generate_answer(
        "Which team made more progressive passes?",
        {"progressive_passes": {"Team A": 10, "Team B": 5}},
    )

    assert captured["model"] == "qwen3:4b"
    assert captured["options"]["temperature"] == 0


def test_generate_answer_includes_question_and_evidence(monkeypatch):
    """The prompt should provide the question and evidence to the model."""
    captured = {}

    def fake_chat(**kwargs):
        captured.update(kwargs)
        return fake_response("Team A made more progressive passes.")

    monkeypatch.setattr("src.agent.chat", fake_chat)

    question = "Which team made more progressive passes?"
    evidence = {
        "progressive_passes": {
            "Team A": 10,
            "Team B": 5,
        }
    }

    generate_answer(question, evidence)

    prompt = captured["messages"][0]["content"]

    assert question in prompt
    assert json.dumps(evidence, indent=2) in prompt


def test_generate_answer_returns_string(monkeypatch):
    """The function should return a string for downstream processing."""
    monkeypatch.setattr(
        "src.agent.chat",
        lambda **kwargs: fake_response("Team A performed better."),
    )

    answer = generate_answer(
        "Compare the teams.",
        {"team_summary": {}},
    )

    assert isinstance(answer, str)
    assert answer != ""


def test_generate_answer_quality_check_detects_missing_metrics():
    from test_answer_quality import evaluate_answer

    evidence = {
        "shot_analysis": {
            "Crystal Palace": {
                "shots": 20,
                "total_xg": 2.665,
                "average_xg_per_shot": 0.133,
            },
            "Everton": {
                "shots": 9,
                "total_xg": 0.592,
                "average_xg_per_shot": 0.066,
            },
        }
    }

    incomplete_answer = (
        "Crystal Palace created better shooting chances than Everton. "
        "Their opportunities were better on average."
    )

    issues = evaluate_answer(incomplete_answer, evidence)

    assert any("0.133" in issue for issue in issues)
    assert any("0.066" in issue for issue in issues)
