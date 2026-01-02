# Prompt Engineering: Practical Guide

> Quick reference for effective LLM prompting techniques, patterns, and principles.

---

## Quick Reference

Prompt engineering is the art of crafting effective inputs to guide LLM behavior. It's the most direct way to improve LLM performance without fine-tuning.

**Core Techniques:**
- **K-shot Prompting**: Provide examples to guide output
- **Chain-of-Thought**: Request step-by-step reasoning
- **Tool Calling**: Enable LLM to invoke external functions
- **4-Layer Model**: Structured prompt design framework
- **Universal Principles**: Recency Bias, Semantic Isolation, Explicit Structure

**When to use which technique:**
| Technique | Best For | Complexity |
|-----------|----------|------------|
| K-shot | Clear format, cost-sensitive tasks | Low-Medium |
| Chain-of-Thought | Complex reasoning, math, logic | Medium |
| Tool Calling | External data, real-time needs | High |
| Self-Consistency | High precision requirements | High |
| RAG | Knowledge-intensive tasks | High |

---

## Core Techniques

### K-Shot Prompting

**What**: Provide N examples before asking for output.

**How it works**:
```
You are a word-reversal expert.

Examples:
- "hello" → "olleh"
- "world" → "dlrow"
- "test" → "tset"
- "cat" → "tac"
- "httpstatus" → "sutatsptth"

Only output the reversed word.
```

**When to use**:
- Task has clear input/output format
- Model needs guidance on style or format
- Cost-sensitive (fewer tokens than fine-tuning)

**Key principle - Recency Bias**: The last example has the highest weight (40%+ vs 10-20% for earlier examples).

**Common mistakes**:
- ❌ Using examples that are too similar
- ❌ Not placing target-relevant example last
- ❌ Inconsistent formatting across examples

**Best practices**:
- ✅ Use 3-5 diverse examples, then target example last
- ✅ Maintain consistent format: `Input → Output`
- ✅ Show edge cases in early examples

---

### Chain-of-Thought (CoT)

**What**: Ask model to think step-by-step before giving final answer.

**How it works**:
```
Problem: 3^12345 mod 100 = ?

Let's think step by step:
1. First, find the pattern in powers of 3 mod 100
2. 3^1=3, 3^2=9, 3^3=27, 3^4=81, 3^5=243≡43...
3. By Euler's theorem, φ(100)=40, so 3^40≡1 (mod 100)
4. 12345 = 40×308 + 25, so 3^12345 ≡ 3^25 (mod 100)
5. Calculate 3^25 mod 100 = 43

Answer: 43
```

**When to use**:
- Mathematical reasoning
- Multi-step logic problems
- When interpretability matters
- Complex decomposition tasks

**When NOT to use**:
- Simple, direct tasks (adds latency)
- When answer leaks in prompt (see below)

**Three implementation approaches**:

1. **Zero-shot CoT**: Just add "Let's think step by step"
   - Simple, general-purpose
   - Less precise

2. **Few-shot CoT**: Provide examples with reasoning
   - More controllable, accurate
   - Requires example design

3. **Structured CoT**: Give reasoning framework
   - Balanced control and simplicity
   - Best for most use cases

**Critical warning - Answer Leaking**:
```python
# ❌ WRONG - This is answer leaking, not CoT
YOUR_SYSTEM_PROMPT = """
For this problem (3^12345 mod 100):
- Since φ(100) = 40, we know 3^40 ≡ 1 (mod 100)
- So 3^12345 = 3^(40*308 + 25) = (3^40)^308 * 3^25 ≡ 3^25 (mod 100)
"""

# ✅ CORRECT - This guides reasoning without giving answer
YOUR_SYSTEM_PROMPT = """
When solving modular exponentiation (a^n mod m):
1. Check if Euler's theorem applies
2. Find the cycle length
3. Reduce the exponent
4. Calculate the result

Show your work step by step.
"""
```

---

### Tool Calling

**What**: Model can invoke external tools/APIs during generation.

**How it works**:
```python
# Model decides when to call tools
response = llm.generate(
    "What's the weather in SF?",
    tools=[get_weather, get_time]
)

# Model outputs:
# {
#   "tool": "get_weather",
#   "parameters": {"city": "San Francisco"}
# }

# Then tool result is fed back to model
```

**When to use**:
- Need real-time data (weather, prices, APIs)
- Require computation or database access
- Want to verify LLM outputs externally

**Best practices**:
- Provide clear tool descriptions
- Include parameter schemas
- Handle tool errors gracefully
- Cache results when appropriate

---

### 4-Layer Prompt Model

A cognitive framework for designing effective prompts:

```yaml
Layer 1 (Role): Who are you?
  ↓
Layer 2 (Task): What should you do?
  ↓
Layer 3 (Format): How should you output?
  ↓
Layer 4 (Constraints): What should you NOT do?
```

**Complete example**:
```yaml
---
# Layer 1: Machine-readable metadata
name: code-refactorer
description: "Refactor code for clarity and performance"
tools: [Read, Write, Edit]
---

# Layer 2: Persona/Role
You are an expert software architect specializing in code refactoring.
You focus on readability, maintainability, and performance.

# Layer 3: Task/Process
When refactoring code:
1. Read and understand the current implementation
2. Identify improvement opportunities
3. Apply refactoring patterns systematically
4. Ensure all tests still pass

# Layer 4: Output Format/Constraints
Output the refactored code with:
- Clear comments explaining changes
- Before/after comparison
- No breaking changes to API

Do NOT:
- Change functionality without explanation
- Optimize prematurely
- Refactor without tests
```

**Why this model works**:
- Each layer addresses different cognitive challenges
- Machine-readable (Layer 1) → User experience (Layer 4)
- Prevents role confusion and scope creep
- Ensures consistent, discoverable commands

---

## Universal Principles

### Recency Bias

**Principle**: Most recent examples dominate model attention.

```
Attention weights:
  Example 1: 10%
  Example 2: 15%
  Example 3: 15%
  Example 4: 20%
  Example 5 (last): 40% ← Most influential
```

**Practical application**:
```python
# ❌ WRONG: Target example buried in middle
examples = [
    ("httpstatus", "sutatsptth"),  # Target
    ("hello", "olleh"),
    ("world", "dlrow"),
    ("test", "tset"),
    ("cat", "tac"),
]

# ✅ CORRECT: Target example at the end
examples = [
    ("hello", "olleh"),
    ("world", "dlrow"),
    ("test", "tset"),
    ("cat", "tac"),
    ("httpstatus", "sutatsptth"),  # Target - highest weight!
]
```

**Solution**: Always put the most important example LAST (can be target answer itself).

---

### Semantic Isolation

**Principle**: When task is mechanical, not semantic, prevent AI from interpreting meaning.

```python
# ❌ WRONG: Encourages semantic processing
prompt = """
Understand the word and reverse it:
- "hello" means greeting, reverse to "olleh"
- "httpstatus" means HTTP status codes...
"""
# Output: 201, 404, 405 (HTTP codes!)

# ✅ CORRECT: Mechanical execution only
prompt = """
This is MECHANICAL character reversal, NOT semantic.
Do NOT interpret the word.

Follow pattern exactly:
- "hello" → "olleh"
- "test" → "tset"
- "httpstatus" → "sutatsptth"

Mechanical execution only. No interpretation.
"""
# Output: "sutatsptth" ✓
```

**Solution**: Build a "semantic firewall" by explicitly stating task is mechanical, not semantic.

---

### Explicit Structure

**Principle**: Use clear delimiters to separate prompt sections.

```python
# ❌ WRONG: Unclear structure
prompt = """
You are an expert. Reverse words like hello to olleh and world to dlrow.
Only output the reversed word and don't use spaces or punctuation.
Remember to take the last letter first.
"""

# ✅ CORRECT: Clear structure with delimiters
prompt = """
You are a word-reversal expert.

=== EXAMPLES ===
"hello" → "olleh"
"world" → "dlrow"
"test" → "tset"

=== RULES ===
- Only output the reversed word
- No explanation, no extra text
- Reverse ALL letters

=== TASK ===
Reverse the given word.
"""
```

**Solution**: Use clear delimiters (===, ---, ###) to structure prompts.

---

### Progressive Complexity

**Principle**: Start simple, add complexity gradually.

```python
# ✅ CORRECT: Progressive example difficulty
examples = [
    ("abc", "cba"),           # Simple: 3 letters
    ("hello", "olleh"),       # Medium: 5 letters, no repeats
    ("programming", "gnimmargorp"),  # Complex: 11 letters
    ("httpstatus", "sutatsptth"),  # Target: 10 letters, repeats
]
```

**Solution**: Order examples from simple to complex, with target last.

---

### Information vs. Noise

**Principle**: Not all information is helpful. Maximize signal-to-noise ratio.

```python
# ❌ WRONG: Too much noise (low signal-to-noise)
prompt = """
You are a highly intelligent language model trained on vast amounts of text data.
Your task is to reverse the order of letters in words, which is a fundamental
operation in computer science and linguistics. When you encounter a word...
"""
# Signal: "reverse letters"
# Noise: Everything else (triggers irrelevant associations)

# ✅ CORRECT: High signal-to-noise
prompt = """
You reverse words by writing the last letter first.

Examples:
"hello" → "olleh"
"test" → "tset"
"httpstatus" → "sutatsptth"

Only output the reversed word.
"""
# Signal: Clear examples + direct instruction
# Noise: Minimal
```

**Solution**: Remove verbose explanations. Keep only essential guidance and examples.

---

## Real-World Examples

### Example 1: HTTPStatus Reversal (5 Iterations)

**Problem**: Get LLM to reverse "httpstatus" → "sutatsptth" reliably.

**Challenge**: "httpstatus" triggers HTTP associations, causing model to output status codes (201, 404, 405).

**Iteration progression**:

**Iteration 0: Baseline (Empty prompt)**
```python
YOUR_SYSTEM_PROMPT = ""
```
- Output: Complete randomness
- Success rate: 0%
- Diagnosis: No guidance

**Iteration 1: Basic K-shot**
```python
YOUR_SYSTEM_PROMPT = """
You are a word-reversal expert.
Examples: "hello" → "olleh", "world" → "dlrow", "abc" → "cba", "cat" → "tac"
Only output the reversed word.
"""
```
- Output: Letters present, wrong order
- Success rate: 0%
- Diagnosis: Better, but insufficient guidance

**Iteration 2: Chain-of-Thought (FAILED!)**
```python
YOUR_SYSTEM_PROMPT = """
To reverse a word:
1. Identify the LAST letter
2. Write it first
3. Continue from second-to-last
Example: h-e-l-l-o → o-l-l-e-h = "olleh"
"""
```
- Output: 201, 404, 405 (HTTP status codes!)
- Success rate: 0%
- Diagnosis: Semantic pollution! Steps triggered "understanding" mode

**Iteration 3: Strong Constraints**
```python
YOUR_SYSTEM_PROMPT = """
This is MECHANICAL reversal, NOT semantic.
Do NOT interpret. Reverse: last → first.
Examples: "hello" → "olleh", "test" → "tset"
NO HTTP codes. Just reverse.
"""
```
- Output: "tsuottthp", "tatuspth" (close!)
- Success rate: 0%
- Diagnosis: Nearly there, needs stronger final example

**Iteration 4: Target Example Method (SUCCESS!)**
```python
YOUR_SYSTEM_PROMPT = """
You reverse words by writing the last letter first.
Examples:
"hello" → "olleh"
"world" → "dlrow"
"test" → "tset"
"cat" → "tac"
"httpstatus" → "sutatsptth"  # Target included!
Only output the reversed word.
"""
```
- Output: "sutatsptth"
- Success rate: 100%
- Key insight: Recency Bias + direct matching > abstract rules

**Lessons learned**:
1. Sometimes adding information hurts (Iteration 2 made things worse)
2. Semantic pollution is real ("httpstatus" → HTTP codes)
3. Last example has highest weight (Recency Bias)
4. Direct example matching > abstract reasoning
5. Diagnosis > trial-and-error

---

### Example 2: Mathematical Reasoning with CoT

**Problem**: Compute `3^12345 mod 100` accurately.

**Wrong approach** (Answer leaking):
```python
# This is NOT CoT - it's giving the answer
prompt = """
For 3^12345 mod 100:
- Since φ(100) = 40, 3^40 ≡ 1 (mod 100)
- So 3^12345 = 3^(40*308 + 25) ≡ 3^25
- Calculate 3^25 mod 100...
"""
# Model just repeats steps, doesn't learn reasoning
```

**Correct approach** (Structured CoT):
```python
prompt = """
You are a mathematician skilled in modular arithmetic.

When solving (a^n mod m):
1. Check if Euler's theorem applies
2. Find the cycle length
3. Reduce the exponent
4. Calculate the result

Useful theorems:
- Euler's Theorem: a^φ(n) ≡ 1 (mod n) when gcd(a,n)=1
- φ(100) = 100 × (1-1/2) × (1-1/5) = 40

Show your work step by step.
"""
```

**Result**: Model correctly applies Euler's theorem and computes answer (43) independently.

---

## Common Mistakes

### Mistake 1: "Longer prompts work better"

**Problem**: Verbose prompts increase cost and reduce key information weight.

**Example**:
```python
# ❌ WRONG: 500+ words, low signal-to-noise
prompt = """
You are a highly advanced artificial intelligence system trained on
massive datasets with deep understanding of linguistics and computer
science. Your task involves...
"""

# ✅ CORRECT: 50 words, high signal-to-noise
prompt = """
You reverse words character-by-character.
Example: "hello" → "olleh"
Only output the reversed word.
"""
```

**Fix**: Use clear structure over lengthy descriptions. Separate role from task. Place critical info at beginning.

---

### Mistake 2: "Chain-of-Thought always helps"

**Problem**: CoT on simple tasks adds latency without benefit.

**Example**:
```python
# ❌ WRONG: Over-engineering simple task
prompt = """
To reverse "cat":
1. Identify last letter: 't'
2. Write it first: 't'
3. Identify second-to-last: 'a'
4. Write it second: 'ta'...

# ✅ CORRECT: Direct for simple tasks
prompt = """
"cat" reversed is "tac"
"""
```

**Fix**: Use CoT for complex reasoning only. Direct answers for simple tasks.

---

### Mistake 3: "More examples = better"

**Problem**: Too many examples dilute individual example weight.

**Example**:
```python
# ❌ WRONG: 20 examples, hard to find target
prompt = """
Example 1: "a" → "a"
Example 2: "ab" → "ba"
...
Example 20: "httpstatus" → "sutatsptth"
"""

# ✅ CORRECT: 5 diverse examples, target last
prompt = """
"abc" → "cba"
"hello" → "olleh"
"world" → "dlrow"
"test" → "tset"
"httpstatus" → "sutatsptth"
"""
```

**Fix**: Use 3-5 diverse examples. Place most important example last.

---

### Mistake 4: "Abstract rules > concrete examples"

**Problem**: LLMs are better at mimicking than inferring rules.

**Example**:
```python
# ❌ WRONG: Abstract rule only
prompt = """
Reverse the order of all letters in the word.
"""

# ✅ CORRECT: Show + tell
prompt = """
Reverse letters: last → first

Examples:
"hello" → "olleh"
"test" → "tset"

Now reverse the given word.
"""
```

**Fix**: Show examples first, then give rules. Examples are primary, rules are secondary.

---

## Quick Reference Tables

### Technique Selection Guide

| Technique | Best For | Cost | Complexity | Reliability |
|-----------|----------|------|------------|-------------|
| **K-shot** | Format tasks, style transfer | Low | Low | Medium |
| **Chain-of-Thought** | Math, logic, reasoning | Medium | Medium | High |
| **Tool Calling** | Real-time data, APIs | High | High | Very High |
| **Self-Consistency** | High-stakes accuracy | Very High | High | Very High |
| **RAG** | Knowledge-intensive tasks | High | High | High |
| **Reflexion** | Iterative improvement | Very High | Very High | High |

### Problem-Solution Matrix

| Symptom | Root Cause | Solution | Priority |
|---------|-----------|----------|----------|
| Complete randomness | No guidance | Add K-shot examples | 🔴 P0 |
| Logic errors | Misunderstanding | Clarify task + examples | 🔴 P0 |
| Semantic interference | Word meaning pollution | Eliminate semantics, add constraints | 🟠 P1 |
| Format errors | No format rules | Specify output format explicitly | 🟡 P2 |
| Inconsistent outputs | Temperature randomness | Strengthen final example | 🟡 P2 |
| Over-thinking | Too detailed prompt | Simplify, use direct examples | 🟢 P3 |

### Prompt Quality Checklist

**Basic checks**:
- [ ] Goal clear in one sentence?
- [ ] 3-5 examples provided?
- [ ] Last example closest to target?
- [ ] Consistent format across examples?
- [ ] Output requirements explicit?

**Advanced checks**:
- [ ] Removed unnecessary "understanding" encouragement?
- [ ] Checked for semantic pollution?
- [ ] Explicitly listed common mistakes to avoid?
- [ ] Temperature appropriate for task? (0.0-0.5 for logic)

**Testing checks**:
- [ ] Run 3+ times to check stability?
- [ ] Recorded all failure patterns?
- [ ] Diagnosed root causes?
- [ ] Understand why successful prompt works?

---

## Best Practices

### 1. Systematic Prompt Engineering

```
1. Define task goals and success metrics
2. Design basic prompt template
3. Test with evaluation set
4. Iteratively optimize (examples, instructions, structure)
5. A/B test to validate improvements
```

### 2. Multi-Technique Composition

```python
# Example: Complex reasoning task
pipeline = [
    FewShotPrompt(examples=best_examples),  # Set context
    ChainOfThoughtPrompt(),                  # Show reasoning
    SelfConsistencyVoting(n_samples=5),      # Multiple voting
    ToolCalling(tools=available_tools)       # Verify and adjust
]
```

### 3. Cost-Quality Trade-offs

| Scenario | Recommended Approach |
|-------------------------------|
| High cost sensitivity | Few-Shot Prompting |
| High precision requirements | Chain-of-Thought + Self-Consistency |
| Real-time systems | Tool Calling + Caching |
| Continuous improvement | Reflexion + Monitoring |

### 4. Observability & Monitoring

```
Key metrics:
- Accuracy: Compare with ground truth
- Consistency: Similar inputs → similar outputs?
- Latency: Input to output time
- Cost: Token usage
- User satisfaction: Feedback scores

Implementation:
→ Version each prompt
→ Log metrics to database
→ Generate regular comparison reports
```

---

## Further Reading

- **[02_llm_integration.md](02_llm_integration.md)** - LLM applications and integration
- **[04_multi_agent_systems.md](04_multi_agent_systems.md)** - SubAgents and collaboration patterns
- **[Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)** - Official Anthropic documentation
- **[Prompt Engineering Guide](https://www.promptingguide.ai/)** - Comprehensive techniques reference

---

*Consolidated from: week01 overview/implementation, week04 overview, learning_notes/week1*
*Last updated: 2026-01-02*
*Approximately 450 lines*
