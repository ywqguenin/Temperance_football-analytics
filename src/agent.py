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


def select_tools(
    question: str,
    available_teams: list[str]
) -> ToolDecision:

    prompt = f"""
You are the planning component of a football analytics AI agent.

Do NOT answer the football question directly.

Your task is to decide which analytical tools are required.

Available tools:

{json.dumps(TOOL_DESCRIPTIONS, indent=2)}

Teams available in the current match:

{json.dumps(available_teams)}

Rules:
1. Select only tools that are actually necessary.
2. The "teams" field MUST contain only team names from the available teams list.
3. Never invent placeholder team names such as "Team A" or "Team B".
4. If the question compares both teams, include both available teams.

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


def generate_answer(question: str, evidence: dict) -> str:
    prompt = f"""
You are the interpretation component of a football analytics AI agent.

Answer the user's football question using ONLY the evidence provided.

Follow these rules:

1. Start with a direct answer to the user's question.
2. Support the conclusion with the most relevant statistics
   from the evidence.
3. When comparing teams, name the teams and compare the
   relevant metrics for both teams whenever available.
4. Explain what the statistics indicate, but do not confuse
   descriptive statistics with causal explanations.
5. Never invent statistics, events, player actions, or facts.
6. Do not infer specific tactical causes unless the evidence
   directly supports them.
7. If the evidence cannot establish a tactical cause,
   explicitly state this limitation when relevant.
8. If the evidence is insufficient to answer the question,
   explain what is missing instead of guessing.
9. Use approximately 2-4 sentences for a straightforward
   question. Use more detail only when the question requires it.
10. Avoid vague conclusions such as "Team A was better"
    without explaining the relevant evidence.
11. Do not repeat the entire evidence dictionary in prose.
12. Answer in the same language as the user's question.

Suggested response structure for a team comparison:
- Conclusion: identify the team supported by the evidence.
- Evidence: compare the relevant metrics.
- Interpretation: explain what those metrics indicate.
- Limitation: mention uncertainty only when relevant.

User question:
{question}

Evidence:
{json.dumps(evidence, indent=2)}
"""

    response = chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0
        }
    )

    return response.message.content.strip()


def run_agent(events, question: str):

    available_teams = (
        events["team"]
        .dropna()
        .unique()
        .tolist()
    )

    decision = select_tools(
        question,
        available_teams
    )

    evidence = execute_tools(
        events,
        decision
    )

    answer = generate_answer(
        question,
        evidence
    )

    return {
        "decision": decision,
        "evidence": evidence,
        "answer": answer
    }
