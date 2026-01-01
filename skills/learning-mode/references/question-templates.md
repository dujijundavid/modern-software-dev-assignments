# Question Templates for Learning Mode

This file contains question templates for different concept complexities. Use these when generating knowledge checks after concept chunks.

## Template Selection Guide

| Complexity | Question Type | When to Use |
|------------|---------------|-------------|
| Simple | Multiple Choice | Basic definitions, single-fact concepts |
| Medium | Open-Ended | Comparisons, "when to use X vs Y" |
| Complex | "Explain in Your Own Words" | Multi-step processes, architecture |
| Application | Scenario-Based | Real-world problem solving |

## Templates

### Template 1: Multiple Choice (Simple Concepts)

```markdown
**Q: [Question]**

a) [Option 1 - plausible distractor]
b) [Option 2 - correct answer]
c) [Option 3 - common misconception]
d) [Option 4 - partially correct but incomplete]

[Hint if needed: Think about X]

**Your answer:** [User responds]
```

**Example**:
```markdown
**Q:** What does the @mcp.tool() decorator do?

a) Creates a new MCP server instance
b) Registers a function as a callable tool for LLMs
c) Connects to an external API
d) Formats the output as JSON

[Hint: Think about what "decorator" means in Python]

**Your answer:**
```

### Template 2: Open-Ended (Medium Concepts)

```markdown
**Q: [Question requiring explanation]**

[Context/Hint if needed]

Try to cover:
- [Point 1]
- [Point 2]

**Your answer:** [User responds]
```

**Example**:
```markdown
**Q:** When would you use an MCP Tool vs. an MCP Resource?

Hint: Tools are for actions (do something), Resources are for data (get something).

Think of a concrete scenario for each...

**Your answer:**
```

### Template 3: "Explain in Your Own Words" (Complex Concepts)

```markdown
**Q: Explain [concept] to someone who [specific context].**

For example: "Explain MCP stdio transport to someone who only knows HTTP APIs."

Don't worry about technical precision - focus on:
1. The core idea
2. Why it's designed this way
3. What trade-offs it makes

**Your explanation:** [User responds]
```

**Example**:
```markdown
**Q:** Explain to a junior developer why MCP servers use stdio instead of HTTP.

Try to cover:
- What stdio means in this context
- The trade-offs (benefits and limitations)
- Why this makes sense for Claude Desktop integration

Don't worry about being perfect - focus on understanding the core idea.

**Your explanation:**
```

### Template 4: Scenario-Based (Application)

```markdown
**Q: You're building [scenario]. How would you use [concept]?

Scenario: [Concrete situation]
Constraints: [Specific limitations]

Walk me through your approach:
1. First, I would...
2. Then, I would...
3. Finally, I would...

**Your approach:** [User responds]
```

**Example**:
```markdown
**Q:** You're building a code review assistant. The user inputs code, and the AI outputs review suggestions.

Which prompting technique would you use and why?

Walk me through your approach:
1. Which technique?
2. Why is it suited for this task?
3. How would you structure the prompt?

**Your approach:**
```

## Adaptive Feedback Patterns

### Correct Answer

```markdown
✓ Exactly right!

[Optional: Add one insight deeper]
"Now, here's an interesting follow-up: What happens if X fails?"
```

### Partially Correct

```markdown
You're on the right track!

[Clarify the missing piece]
"The part about X is correct. Now consider Y..."
```

### Incorrect

```markdown
Not quite - let's revisit this together.

[Provide targeted explanation, not full re-explanation]
"The key insight is..."
```

## Question Generation Tips

1. **Align with learning goal**: If goal is "understand architecture", ask structural questions
2. **Build on examples**: Reference the code example shown in the concept chunk
3. **Test understanding, not memory**: Ask "why" and "how", not just "what"
4. **Provide hints strategically**: Give just enough to guide, not give away
5. **Adapt follow-ups**: Next question should target knowledge gaps revealed
