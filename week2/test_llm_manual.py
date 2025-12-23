"""
Manual test script for extract_action_items_llm()
Run with: poetry run python week2/test_llm_manual.py
"""

from app.services.extract import extract_action_items_llm

# Test Case 1: Bullet points with checkboxes
test_notes_1 = """
Meeting notes from team standup:
- [ ] Set up the database schema
* Implement the API extract endpoint
1. Write comprehensive tests
Some general context about the project.
"""

print("=" * 60)
print("TEST CASE 1: Bullet points and checkboxes")
print("=" * 60)
result_1 = extract_action_items_llm(test_notes_1)
print(f"\n✅ Result: {result_1}\n")

# Test Case 2: Keywords (TODO, action)
test_notes_2 = """
TODO: Review pull requests
action: Fix bug #123
next: Schedule team meeting
Also we had a great discussion about the roadmap.
"""

print("=" * 60)
print("TEST CASE 2: Keywords (TODO, action, next)")
print("=" * 60)
result_2 = extract_action_items_llm(test_notes_2)
print(f"\n✅ Result: {result_2}\n")

# Test Case 3: Mixed format
test_notes_3 = """
Project brainstorming session:
We need to improve performance. 
- Optimize database queries
The current implementation is slow.
TODO: Add caching layer
Consider using Redis for session storage.
"""

print("=" * 60)
print("TEST CASE 3: Mixed format (narrative + actionable)")
print("=" * 60)
result_3 = extract_action_items_llm(test_notes_3)
print(f"\n✅ Result: {result_3}\n")

# Test Case 4: Empty input
test_notes_4 = ""

print("=" * 60)
print("TEST CASE 4: Empty input")
print("=" * 60)
result_4 = extract_action_items_llm(test_notes_4)
print(f"\n✅ Result: {result_4}\n")

# Test Case 5: No action items
test_notes_5 = """
The meeting was very productive.
Everyone agreed on the timeline.
We're making good progress.
"""

print("=" * 60)
print("TEST CASE 5: No actionable items")
print("=" * 60)
result_5 = extract_action_items_llm(test_notes_5)
print(f"\n✅ Result: {result_5}\n")

print("=" * 60)
print("🎉 All manual tests completed!")
print("=" * 60)
