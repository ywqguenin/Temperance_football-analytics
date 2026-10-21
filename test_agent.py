from src.agent import run_agent
from src.data_loader import (
    load_matches,
    get_match_options,
    load_match_events,
)


def main():
    competition_id = 2
    season_id = 27

    matches = load_matches(
        competition_id,
        season_id
    )

    options = get_match_options(matches)

    print("\n--- AVAILABLE MATCHES ---")
    print(
        options.head(20).to_string(index=False)
    )

    selected_match_id = int(
        input("\nEnter match ID: ")
    )

    selected_match = options[
        options["match_id"] == selected_match_id
    ]

    if selected_match.empty:
        raise ValueError(
            f"Match {selected_match_id} not found "
            f"in competition {competition_id}, season {season_id}."
        )

    print("\n--- SELECTED MATCH ---")
    print(
        selected_match.to_string(index=False)
    )

    events = load_match_events(
        selected_match_id
    )

    question = input(
        "\nAsk a football question: "
    )

    result = run_agent(
        events,
        question
    )

    print("\n--- AGENT PLAN ---")
    print("Tools:", result["decision"].tools)
    print("Teams:", result["decision"].teams)
    print("Reason:", result["decision"].reason)

    print("\n--- EVIDENCE ---")
    print(result["evidence"])

    print("\n--- FINAL ANSWER ---")
    print(result["answer"])


if __name__ == "__main__":
    main()
