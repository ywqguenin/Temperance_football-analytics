from statsbombpy import sb

from src.agent import (
    select_tools,
    execute_tools
)


match_id = 3754296
events = sb.events(match_id=match_id)


question = (
    "Why did Arsenal create fewer shots but still produce "
    "higher total xG than Manchester City?"
)


decision = select_tools(question)

print("\n--- AGENT PLAN ---")
print("Tools:", decision.tools)
print("Teams:", decision.teams)
print("Reason:", decision.reason)


evidence = execute_tools(
    events,
    decision
)

print("\n--- EVIDENCE ---")
print(evidence)
