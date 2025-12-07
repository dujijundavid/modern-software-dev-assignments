import os
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 10

# TODO: Fill this in!
YOUR_SYSTEM_PROMPT = """You reverse words by writing the last letter first, then the second-to-last, and so on.

Examples:
"hello" → "olleh"
"world" → "dlrow"  
"test" → "tset"
"cat" → "tac"
"httpstatus" → "sutatsptth"

Remember: 
- Only output the reversed word
- No explanation, no extra text
- Just reverse the order of all letters"""

USER_PROMPT = """
Reverse the order of letters in the following word. Only output the reversed word, no other text:

httpstatus
"""


EXPECTED_OUTPUT = "sutatsptth"

def test_your_prompt(system_prompt: str) -> tuple[int, int]:
    """Run the prompt NUM_RUNS_TIMES and return (success_count, total_runs).

    Continues running all iterations regardless of success.
    Prints summary with pass rate at the end.
    """
    success_count = 0
    for idx in range(NUM_RUNS_TIMES):
        print(f"Running test {idx + 1} of {NUM_RUNS_TIMES}")
        response = chat(
            model="mistral-nemo:12b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.5},
        )
        output_text = response.message.content.strip()
        if output_text.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            success_count += 1
        else:
            print(f"Expected output: {EXPECTED_OUTPUT}")
            print(f"Actual output: {output_text}")
    
    # Display final pass rate summary
    pass_rate = (success_count / NUM_RUNS_TIMES) * 100
    print(f"\n{'='*50}")
    print(f"Final Results: {success_count}/{NUM_RUNS_TIMES} tests passed ({pass_rate:.1f}%)")
    print(f"{'='*50}")
    
    return success_count, NUM_RUNS_TIMES

if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)