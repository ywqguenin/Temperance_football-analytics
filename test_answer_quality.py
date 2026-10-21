
import re
import math

from src.agent import generate_answer


# Fixed evidence makes the evaluation reproducible.
QUESTION = "Which team created better shooting chances?"

EVIDENCE = {
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


def extract_numbers(value):
    """Recursively extract numeric values from nested evidence."""
    numbers = []

    if isinstance(value, dict):
        for item in value.values():
            numbers.extend(extract_numbers(item))
    elif isinstance(value, (list, tuple)):
        for item in value:
            numbers.extend(extract_numbers(item))
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        numbers.append(float(value))

    return numbers


def evaluate_answer(answer, evidence):
    """Run basic, transparent checks on the generated answer."""
    issues = []
    answer_lower = answer.lower()

    # Check 1: Is the answer substantial enough to evaluate?
    if len(answer.split()) < 15:
        issues.append("Answer may be too short.")

    # Check 2: Does it mention both teams?
    for team in evidence["shot_analysis"]:
        if team.lower() not in answer_lower:
            issues.append(f"Missing team name: {team}")

    # Check 3: Check whether the answer cites the most relevant metrics.
    # Average xG per shot is the primary metric for this question.
    required_values = ["0.133", "0.066"]

    for value in required_values:
        if value not in answer:
            issues.append(
                f"Primary metric not explicitly cited: {value}"
            )

    # Total xG provides useful additional context, but is optional.
    optional_values = ["2.665", "0.592"]

    missing_optional = [
        value for value in optional_values
        if value not in answer
    ]

    if missing_optional:
        print(
            "[INFO] Optional supporting metrics omitted:",
            ", ".join(missing_optional)
        )

    # Check 4: Are all numeric claims supported by the evidence?
    evidence_numbers = extract_numbers(evidence)
    answer_numbers = re.findall(r"(?<!\w)-?\d+(?:\.\d+)?", answer)

    unsupported_numbers = []

    for token in answer_numbers:
        number = float(token)

        supported = any(
            math.isclose(number, value, abs_tol=0.005, rel_tol=0)
            for value in evidence_numbers
        )

        if not supported:
            unsupported_numbers.append(token)

    if unsupported_numbers:
        issues.append(
            "Potentially unsupported numeric claims: "
            + ", ".join(unsupported_numbers)
        )

    return issues


def main():
    print("Generating answer with Qwen3:4b...")
    print("Question:", QUESTION)

    answer = generate_answer(QUESTION, EVIDENCE)

    print("\n--- GENERATED ANSWER ---")
    print(answer)

    issues = evaluate_answer(answer, EVIDENCE)

    print("\n--- QUALITY CHECKS ---")

    if not issues:
        print("All basic checks passed.")
    else:
        for issue in issues:
            print("[REVIEW]", issue)

    print("\n--- EVALUATION SUMMARY ---")
    print("Word count:", len(answer.split()))
    print("Basic checks passed:", len(issues) == 0)
    print("Review items:", len(issues))


if __name__ == "__main__":
    main()
