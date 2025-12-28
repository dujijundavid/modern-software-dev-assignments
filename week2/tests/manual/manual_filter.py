from week2.app.services.extract import extract_action_items


def main() -> None:
    """Run manual sanity checks for rule-based filtering."""
    # Test with problematic input
    text = """* deploy app
- set up database
- 你是谁
- helloworlda's'da's'da's'da"""

    result = extract_action_items(text)
    print(f"Filtered result: {result}")
    print(f"Count: {len(result)}")

    # Test edge cases
    print("\nEdge case tests:")
    tests = [
        ("- deploy app", "Valid action"),
        ("- set up database", "Valid action"),
        ("- 你是谁", "Chinese (should pass - enough alpha)"),
        ("- a'a'a'a'a", "Repetitive (should fail)"),
        ("- ???", "Only symbols (should fail)"),
        ("- x", "Too short (should fail)"),
        ("- Is this a question?", "Question mark (should fail)"),
    ]

    for text, desc in tests:
        result = extract_action_items(text)
        status = "✓" if result else "✗"
        print(f"{status} {desc}: '{text}' -> {result}")


if __name__ == "__main__":
    main()
