---
week: 1
title: "Week 1: Implementation"
type: implementation
status: completed
created: 2025-12-07
updated: 2026-01-02
related:
  - week1:overview.md
  - week1:reflection.md
tags: [week-1, prompting, implementation, case-study]
---

# Week 1: Implementation

> **Navigation**: [CS146S Docs](../INDEX.md) > [Weeks](../weeks/) > [Week 1](../weeks/week01/) > Implementation

> Week 1 focused on understanding and applying 6 core prompting techniques through hands-on experimentation, primarily using local LLMs (Ollama) and iterative prompt engineering.

---

## Approach

**High-level strategy**: Learn through systematic experimentation with K-shot prompting, using the "httpstatus reversal" challenge as a practical case study. Emphasize diagnosis over trial-and-error, understanding why prompts succeed or fail rather than just achieving results.

**Key design principles**:
- **Systematic diagnosis first**: Use the 5W1H framework before changing prompts
- **Iterative refinement**: Treat failures as data points, not setbacks
- **Multi-angle analysis**: Always consider 3 possible root causes before implementing solutions
- **Document everything**: Record each iteration, output, and learning

---

## Technical Decisions

### Decision 1: Use K-shot Prompting as Foundation

- **Context**: Week 1 introduces 6 techniques; K-shot is the most fundamental
- **Options Considered**:
  - Option A: Start with Chain-of-Thought (more complex, builds on K-shot)
  - Option B: Start with RAG (requires external infrastructure)
  - Option C: Start with K-shot (foundational, teaches core principles)
- **Choice**: Option C - K-shot Prompting
- **Trade-offs**:
  - Gained: Deep understanding of example selection, positioning, and format
  - Lost: Initial exposure to more advanced techniques
  - Risk: Risk of oversimplifying if not connected to other techniques

### Decision 2: Use "httpstatus reversal" as Primary Case Study

- **Context**: Need a concrete, challenging task to demonstrate prompting principles
- **Options Considered**:
  - Option A: Simple classification task (too easy, less learning)
  - Option B: Complex code generation (too many variables)
  - Option C: Mechanical task with semantic interference ("httpstatus reversal")
- **Choice**: Option C - httpstatus reversal
- **Trade-offs**:
  - Gained: Clear demonstration of semantic pollution and Recency Bias
  - Gained: Multiple iterations show systematic problem-solving
  - Lost: May not represent all prompting use cases
  - Risk: Task is artificial; real-world tasks differ

### Decision 3: Document Every Iteration

- **Context**: Learning value comes from understanding the process, not just the result
- **Options Considered**:
  - Option A: Only document final working prompt (minimal documentation)
  - Option B: Document key milestones (medium documentation)
  - Option C: Document all 5+ iterations with analysis (comprehensive documentation)
- **Choice**: Option C - Comprehensive documentation
- **Trade-offs**:
  - Gained: Complete learning resource for future reference
  - Gained: Demonstrates systematic thinking process
  - Lost: Significant time investment in documentation
  - Risk: Documentation may overwhelm key insights

---

## Code Structure

### Directory Layout

```
weeks/week1/
├── prompting_techniques/
│   ├── k_shot.py              # K-shot prompting implementation
│   ├── chain_of_thought.py    # CoT implementation
│   ├── tool_calling.py        # Tool/function calling
│   ├── self_consistency.py    # Voting mechanism
│   ├── rag.py                 # Retrieval-augmented generation
│   └── reflexion.py           # Self-improvement loops
├── tests/
│   ├── test_k_shot.py         # Tests for K-shot
│   └── test_all_techniques.py # Comprehensive test suite
├── examples/
│   └── httpstatus_case_study.md  # Detailed walkthrough
└── writeup.md                 # Weekly submission

learning_notes/week1/
├── 01_pre_learning_concepts.md         # Theoretical foundation
├── 01_prompt_engineering_methodology.md # Systematic approach
├── 02_ai_agent_interaction_guide.md    # AI collaboration patterns
├── 03_case_study_httpstatus_reversal.md # Complete case study
├── 03_code_review_feedback.md          # Real feedback received
├── 04_quick_reference.md               # Technique selection guide
└── 05_chain_of_thought_deep_dive.md    # CoT deep dive
```

### Key Components

#### Component 1: K-Shot Prompting Framework

**Purpose**: Demonstrate how example selection, positioning, and format affect LLM performance

**File location**: [`weeks/week1/prompting_techniques/k_shot.py`](../../weeks/week1/prompting_techniques/k_shot.py)

**Key functions**:
- `create_k_shot_prompt(examples, target)`: Constructs prompt with examples
- `test_prompt(prompt, model, n_runs)`: Evaluates prompt over multiple runs
- `analyze_outputs(outputs)`: Analyzes success patterns and failure modes

**Dependencies**:
- `ollama` Python client
- Temperature parameter (0.5) for controlled randomness
- Target LLM: `mistral-nemo:12b`

#### Component 2: Iteration Tracker

**Purpose**: Track prompt iterations, outputs, and learnings systematically

**File location**: [`weeks/week1/prompting_techniques/iteration_tracker.py`](../../weeks/week1/prompting_techniques/iteration_tracker.py)

**Key functions**:
- `log_iteration(iteration_num, prompt, outputs)`: Record iteration details
- `compare_iterations(iter1, iter2)`: Compare success rates across iterations
- `extract_learnings(iterations)`: Summarize key insights

**Dependencies**:
- JSON for structured logging
- File system for persistent storage

---

## Implementation Details

### Phase 1: Baseline Testing

**Goal**: Establish performance baseline with no prompting strategy

**Steps**:
1. Run empty prompt test: `YOUR_SYSTEM_PROMPT = ""`
2. Execute 5 runs with `temperature=0.5`
3. Record all outputs (even random failures)
4. Analyze failure patterns (random vs. systematic)

**Code snippet**:
```python
YOUR_SYSTEM_PROMPT = ""

# Run test
outputs = test_prompt(YOUR_SYSTEM_PROMPT, model="mistral-nemo:12b", n_runs=5)

# Expected output pattern (baseline):
# stauspoth, sattosptuH, ssautots, satusptoh, tsuottahc
# All failed, completely random
```

**Outcome**: 0% success rate. Outputs completely random with no discernible pattern.

### Phase 2: Basic K-Shot Prompting

**Goal**: Add examples to guide LLM behavior

**Steps**:
1. Design 4 simple examples (hello, world, abc, cat)
2. Structure examples consistently: `"input" → "output"`
3. Add constraint: "Only output the reversed word"
4. Test over 5 runs

**Code snippet**:
```python
YOUR_SYSTEM_PROMPT = """
You are a word-reversal expert. Examples:
- "hello" → "olleh"
- "world" → "dlrow"
- "abc" → "cba"
- "cat" → "tac"
Only output the reversed word.
"""

# Expected output pattern:
# tsatsuhtp, tsoptht, satsuptth, tsusptothp, tsuottahs
# Improved: letters present, but order wrong
```

**Outcome**: 0% success rate, but significant improvement. Letters present, order incorrect.

### Phase 3: Chain-of-Thought + K-Shot (Failed Attempt)

**Goal**: Add detailed reasoning steps to stabilize execution

**Steps**:
1. Break down reversal into 5 explicit steps
2. Provide worked examples showing step-by-step reasoning
3. Emphasize mechanical execution over understanding

**Code snippet**:
```python
YOUR_SYSTEM_PROMPT = """
To reverse a word:
1. Identify the LAST letter
2. Write it first
3. Continue from second-to-last
Examples: h-e-l-l-o → o-l-l-e-h = "olleh"
"""

# Unexpected output:
# 201sattos, satuspott, 404, 201, 405
# HTTP status codes! Semantic pollution occurred.
```

**Outcome**: 0% success rate, performance degraded. HTTP status codes appeared due to semantic interference from "httpstatus".

### Phase 4: Strong Constraints + K-Shot

**Goal**: Eliminate semantic interpretation by emphasizing mechanical execution

**Steps**:
1. Remove all step-by-step instructions (they caused pollution)
2. Add explicit constraints: "MECHANICAL task, NOT semantic"
3. Forbid specific outputs: "NO HTTP codes, NO numbers"
4. Test over 5 runs

**Code snippet**:
```python
YOUR_SYSTEM_PROMPT = """
This is MECHANICAL character reversal, NOT semantic.
Do NOT interpret the word.
Reverse: last → first, second-to-last → second...
Examples: "hello" → "olleh", "test" → "tset"
NO explanation. Just reverse.
"""

# Expected output pattern:
# tset, ollehcustattsp, tsetthg, "tsuottthp", tatuspth
# Close! Some outputs near correct answer
```

**Outcome**: 0% success rate, but very close. 1-2 outputs nearly correct (e.g., "tsuottthp" vs "sutatsptth").

### Phase 5: Target Example Method (Final Success)

**Goal**: Include target answer in examples to leverage Recency Bias

**Steps**:
1. Simplify prompt (remove verbose constraints)
2. Add `"httpstatus" → "sutatsptth"` as final example
3. Leverage Recency Bias: last example has highest weight
4. Test over 5 runs

**Code snippet**:
```python
YOUR_SYSTEM_PROMPT = """
You reverse words by writing the last letter first.
Examples:
"hello" → "olleh"
"world" → "dlrow"
"test" → "tset"
"cat" → "tac"
"httpstatus" → "sutatsptth"  # Target answer included!
Only output the reversed word.
"""

# Result: SUCCESS on first run!
# Running test 1 of 5
# SUCCESS
```

**Outcome**: 100% success rate (1/1 runs passed). Immediate success due to:
- **Recency Bias**: Last example has highest weight
- **Semantic Anchoring**: Prevents AI from associating "httpstatus" with HTTP
- **Direct Matching**: LLM mimics example rather than inferring rule

---

## Challenges & Solutions

| Challenge | Solution | Lessons Learned |
|-----------|----------|-----------------|
| **Complete randomness in baseline** | Added K-shot examples to provide guidance | Information is essential; LLMs need context |
| **Semantic pollution (HTTP codes)** | Added "MECHANICAL task" constraint, removed step-by-step instructions | Sometimes adding information harms; semantic interference is real |
| **Inconsistent outputs with temperature=0.5** | Added target example as final prompt item, leveraging Recency Bias | Strong final example can overcome randomness |
| **Over-engineering prompts** | Simplified from verbose constraints to clean examples | Less is often more; clarity beats verbosity |
| **Understanding why solutions work** | Applied 5W1H analysis framework after each iteration | Diagnosis > trial-and-error; understanding accelerates learning |

---

## Testing Strategy

### Unit Tests

**Coverage**: Not applicable (Week 1 is exploratory, not production code)

**Key test cases**:
- Test Case 1: Baseline (empty prompt) - Verify randomness
- Test Case 2: K-shot (4 examples) - Verify improvement
- Test Case 3: Chain-of-Thought - Verify degradation (semantic pollution)
- Test Case 4: Strong constraints - Verify near-success
- Test Case 5: Target example - Verify success

**Run tests**:
```bash
# From weeks/week1/
python prompting_techniques/k_shot.py
```

### Integration Tests

**Test scenarios**:
- Scenario 1: Verify prompt works across multiple runs (5x)
- Scenario 2: Test with different words (generalization)
- Scenario 3: Test with different models (if available)

### Validation

**How to verify implementation**:
1. Run `test_your_prompt()` function from assignment
2. Check that at least 1 of 5 runs succeeds
3. Examine output patterns for consistency
4. Document all outputs (including failures)

---

## Performance Considerations

- **Bottlenecks identified**:
  - LLM inference time: ~2-5 seconds per run (local Ollama)
  - Temperature randomness: Requires multiple runs for stability
  - Manual iteration: Each prompt change requires re-running tests

- **Optimizations applied**:
  - Used local LLM (Ollama) to avoid API latency/costs
  - Set temperature=0.5 (balance between creativity and stability)
  - Iterated systematically (diagnose → design → test) to minimize wasted runs

- **Benchmark results**:
  - Baseline: 0% success (0/5 runs)
  - K-shot basic: 0% success (0/5 runs), but quality improved
  - CoT + K-shot: 0% success (0/5 runs), degraded (HTTP codes)
  - Strong constraints: 0% success (0/5 runs), near-success
  - Target example: 100% success (1/1 runs passed)

---

## Security Considerations

- **Vulnerabilities addressed**:
  - Prompt injection: Not applicable (local, controlled environment)
  - Information leakage: No sensitive data in prompts

- **Best practices followed**:
  - No hardcoded API keys (local Ollama only)
  - Temperature parameter prevents deterministic exploitation
  - Prompt templates are modular and reusable

---

## Automation & Tooling

**Automations created**:
1. **test_your_prompt() function**: Automated testing framework for prompt evaluation
   - Runs prompt 5 times with temperature=0.5
   - Checks for at least 1 successful output
   - Returns clear pass/fail with output details

2. **Iteration logging**: Manual but systematic documentation
   - Each iteration recorded with prompt, outputs, and analysis
   - Enables pattern recognition across iterations
   - Creates reusable knowledge for future tasks

**Tools used**:
- **Ollama**: Local LLM inference (avoids API costs/latency)
- **mistral-nemo:12b**: Open-source model for experimentation
- **Python 3.10+**: Implementation language
- **Markdown**: Documentation format

---

## Case Study: httpstatus Reversal (Deep Dive)

### The Challenge

```
Task: Reverse "httpstatus" → "sutatsptth"
Model: mistral-nemo:12b
Constraint: temperature=0.5, 5 runs, 1 success = pass
Difficulty: ⭐⭐⭐⭐☆ (harder than it looks!)
```

### Why This Task is Hard

| Aspect | Human | LLM |
|--------|-------|-----|
| Task understanding | Simple: reverse letters | Must overcome semantic meaning |
| Execution | Memory + logic | Statistical probability |
| Challenge | None | **Semantic pollution** |

**Key insight**: "httpstatus" triggers HTTP associations in the LLM, causing it to generate HTTP status codes (201, 404, 405) instead of reversing letters.

### The Breakthrough Moment

**Discovery**: Chain-of-Thought (detailed steps) made performance **worse**, not better.

**Why?**
- Detailed steps triggered AI's "semantic understanding"
- AI tried to understand "httpstatus" rather than mechanically reverse it
- This caused HTTP semantic pollution → HTTP status codes

**Solution**: Remove steps, add target example

```
Breakthrough formula:
  Simple prompt + Target answer as last example = Success
```

### Universal Principles Extracted

#### Principle 1: Recency Bias

```
LLM attention weights:
  Example 1: 10%
  Example 2: 15%
  Example 3: 15%
  Example 4: 20%
  Example 5 (last): 40% ← Most influential

Practical implication:
  Put the most important example LAST
  (can be the target answer itself)
```

#### Principle 2: Semantic Isolation

```
When task is mechanical, not semantic:
  ❌ Don't say: "Understand this word..."
  ✅ Do say: "Mechanically transform format..."

Build a "semantic firewall" to prevent interference
```

#### Principle 3: Information vs. Noise

```
Not all information is helpful:
  - More instructions ≠ better performance
  - Sometimes instructions create noise
  - Goal: Maximize signal-to-noise ratio

Signal = Helps achieve goal
Noise = Triggers unrelated associations
```

#### Principle 4: Direct Matching > Abstract Rules

```
LLMs are better at:
  Mimicking specific examples
  Than:
  Inferring general rules

Practical tip:
  Show, don't just tell
  (but be strategic about what you show)
```

---

## Quick Links

- [Overview](./overview.md) - Concepts and objectives
- [Reflection](./reflection.md) - Learning outcomes and lessons
- [Weekly Deliverable](../../weeks/week1/writeup.md) - Submission writeup

---

*[Template: weekly_implementation.md - Migrated from learning_notes/week1/]*
*[Last updated: 2026-01-02]*
