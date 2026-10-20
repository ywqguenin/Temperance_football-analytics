from src.agent import run_agent
from src.data_loader import load_match_events


def main():
    match_id = 3754296

    # Load match data from local cache.
    # If the cache does not exist, it will download from StatsBomb
    # and save the data locally.
    events = load_match_events(match_id)

    question = (
        "Which team had the stronger overall attacking "
        "and passing performance?"
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
