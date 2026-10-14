import json
from ollama import chat
from typing import Literal
from pydantic import BaseModel

from src.tool_registry import TOOL_DESCRIPTIONS

from src.analysis_tools import (
    build_team_summary,
    get_final_third_entries,
    get_progressive_passes,
)


ToolName = Literal[
    "team_summary",
    "shot_analysis",
    "final_third_entries",
    "progressive_passes"
]


class ToolDecision(BaseModel):
    tools: list[ToolName]
    teams: list[str]
    reason: str


def execute_tools(events, decision: ToolDecision):

    evidence = {}

    for tool in decision.tools:

        if tool == "shot_analysis":

            evidence["shot_analysis"] = {}

            for team in decision.teams:
                summary = build_team_summary(events, team)

                evidence["shot_analysis"][team] = {
                    "shots": summary["shots"],
                    "total_xg": summary["total_xg"],
                    "average_xg_per_shot":
                        summary["average_xg_per_shot"]
                }

        elif tool == "final_third_entries":

            evidence["final_third_entries"] = {}

            for team in decision.teams:
                entries = get_final_third_entries(
                    events,
                    team
                )

                evidence["final_third_entries"][team] = len(entries)

        elif tool == "progressive_passes":

            evidence["progressive_passes"] = {}

            for team in decision.teams:
                progressive = get_progressive_passes(
                    events,
                    team
                )

                evidence["progressive_passes"][team] = len(
                    progressive
                )

        elif tool == "team_summary":

            evidence["team_summary"] = {}

            for team in decision.teams:
                evidence["team_summary"][team] = (
                    build_team_summary(events, team)
                )

    return evidence


def select_tools(question: str) -> ToolDecision:

    prompt = f"""
You are the planning component of a football analytics AI agent.

Do NOT answer the football question directly.

Your task is to decide which analytical tools are required.

Available tools:

{json.dumps(TOOL_DESCRIPTIONS, indent=2)}

Select only tools that are actually necessary.

User question:
{question}
"""

    response = chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format=ToolDecision.model_json_schema(),
        options={
            "temperature": 0
        }
    )

    return ToolDecision.model_validate_json(
        response.message.content
    )
