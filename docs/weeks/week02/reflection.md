---
week: 2
title: "Week 2: Reflection"
type: reflection
status: completed
created: 2025-12-28
updated: 2026-01-02
related:
  - week:2:overview.md
  - week:2:implementation.md
tags: [week-2, reflection, learning-outcomes]
---

# Week 2: Reflection

> **Navigation**: [CS146S Docs](../../INDEX.md) > [Weeks](../weeks/) > [Week 2](../weeks/week02/) > Reflection

## What I Learned

### Technical Skills

- **LLM Integration with Structured Output**: Learned to use JSON Schema with Ollama to guarantee parseable responses from LLMs
  - How I applied it: Implemented `extract_action_items_llm()` with `format='json'` and schema validation
  - Resources that helped: [Ollama Structured Outputs blog](https://ollama.com/blog/structured-outputs), trial and error with different schemas
  - Confidence level: 4/5 - Comfortable with basic schemas, need more practice with complex nested structures

- **Testing Strategy with Mock**: Mastered the testing pyramid for LLM applications (70% Mock, 20% real LLM, 10% edge cases)
  - How I applied it: Wrote 5 fast Mock tests using `@patch` decorator, 2 slow integration tests
  - Resources that helped: `learning_notes/week2/practice/testing_patterns.md`, Python `unittest.mock` documentation
  - Confidence level: 5/5 - Clear understanding of when to Mock vs when to use real dependencies

- **Pydantic for Type Safety**: Learned to use Pydantic schemas for request/response validation in FastAPI
  - How I applied it: Created schemas for all API contracts (NoteCreate, ExtractRequest, ActionItemResponse, etc.)
  - Resources that helped: FastAPI documentation on request bodies, Pydantic docs on field validation
  - Confidence level: 4/5 - Comfortable with basic models, learning more about advanced features (validators, root_model)

- **Refactoring Patterns**: Transformed working code into maintainable, layered architecture
  - How I applied it: Separated Router, Service, and Database layers; added factory methods; created custom exceptions
  - Resources that helped: `learning_notes/week2/practice/refactoring_journey.md`, code review feedback
  - Confidence level: 3/5 - Understand principles, but need more practice identifying refactoring opportunities

- **FastAPI Exception Handlers**: Implemented global error handling with custom exceptions
  - How I applied it: Created `DatabaseError` and `NotFoundError` with context, registered handlers in `main.py`
  - Resources that helped: FastAPI docs on exception handlers, trial and error
  - Confidence level: 4/5 - Confident in basic handlers, want to learn more about exception chaining

### AI Engineering Concepts

- **Structured Output is Non-Negotiable**: For production LLM applications, structured output is essential not optional
  - Real-world application: Any LLM feature that integrates with databases, APIs, or internal systems
  - Connection to course themes: Building reliable systems that work consistently, not toy demos

- **Testing Pyramid Applies to LLM Apps**: The classic testing pyramid (many unit tests, fewer integration tests) applies to LLM applications
  - Real-world application: LLM-powered features in production need fast feedback loops during development
  - Connection to course themes: Automation and speed - Mock tests are 60x faster, enabling rapid iteration

- **Layered Architecture Isolates Changes**: Separating concerns (Router, Service, Database) makes it easier to swap implementations
  - Real-world application: Switching from llama3.1:8b to GPT-4 only requires changing the service layer
  - Connection to course themes: Building composable systems that can evolve without rewriting everything

- **Graceful Degradation Over Crashing**: When LLM APIs fail, return empty results rather than crashing the application
  - Real-world application: Production systems must be resilient to external service failures
  - Connection to course themes: Building robust systems that handle errors gracefully

### Automation & Systems Thinking

**Automations I built/used**:
1. Mock test pattern: Reusable `@patch` decorator pattern for fast unit tests (saves ~20s per test run)
2. Pydantic schema template: Reusable schema structure for request/response models (saves ~10 min per new endpoint)
3. Factory method pattern: `from_dict()` classmethod for converting DB dicts to Pydantic models (saves ~5 lines per model)
4. LLM extraction wrapper: Reusable function for structured output with any schema (saves ~30 min vs implementing from scratch)

**Systems thinking insights**:
- Insight 1: Building systems means designing for failure (LLM timeouts, invalid JSON), not just happy paths
- Insight 2: Composability requires clear interfaces (dict vs Row), not just sharing data structures
- Insight 3: Leverage points in testing are where external dependencies are called (Mock those, test everything else)

## What I'd Do Differently

### Mistake 1: Initially Using Only Real LLM Tests

- **What happened**: Started with 7 tests all using real Ollama calls, took 21 seconds to run
- **Root cause**: Didn't know about Mock testing strategy for external dependencies
- **Impact**: Slow feedback loop during development, wasted time waiting for tests
- **How I'd fix it**: Start with Mock tests, add real LLM tests later for integration validation
- **Prevention strategy**: Always identify external dependencies first (LLM APIs, databases), plan to Mock them
- **Automation opportunity**: Create a checklist: "Does this test call external service? If yes, Mock it first"

### Mistake 2: Not Designing Schemas Upfront

- **What happened**: Built endpoints with `Dict[str, Any]`, then had to refactor to add Pydantic schemas
- **Root cause**: Rushed to implement features without designing contracts first
- **Impact**: Refactoring took 2-3 hours, could have been done upfront in 30 minutes
- **How I'd fix it**: Design schemas before implementing endpoints
- **Prevention strategy**: Start with contract design (schemas), then implement logic
- **Automation opportunity**: Create a FastAPI project template with example schemas

### Mistake 3: Over-Engineering Exception Classes

- **What happened**: Initially created complex exception hierarchy with custom serialization
- **Root cause**: Thought more complex = better design
- **Impact**: Spent 1 hour on exceptions, simplified to 2 classes (DatabaseError, NotFoundError)
- **How I'd fix it**: Start simple, add complexity only when needed
- **Prevention strategy**: YAGNI principle - You Ain't Gonna Need It (yet)
- **Automation opportunity**: None - this is a judgment call, better learned through experience

## Time Allocation

| Activity | Estimated | Actual | Variance | Notes |
|----------|-----------|--------|----------|-------|
| LLM integration (extract.py) | 3 hrs | 4 hrs | +1 hr | Debugging JSON schema took longer |
| Writing tests (test_extract.py) | 2 hrs | 3 hrs | +1 hr | Learned Mock patterns, added edge cases |
| Refactoring (schemas, db.py) | 2 hrs | 2.5 hrs | +0.5 hr | Factory methods took time to get right |
| Exception handlers (main.py) | 1 hr | 0.5 hr | -0.5 hr | Faster once pattern was clear |
| Frontend (index.html) | 1 hr | 0.5 hr | -0.5 hr | Simple UI, reused patterns |
| Documentation (README, writeup) | 2 hrs | 2.5 hrs | +0.5 hr | Writing takes time |
| **Total** | **11 hrs** | **13 hrs** | **+2 hrs** | Overall reasonable estimate |

**Time allocation insights**:
- Insight 1: Learning new patterns (Mock testing) always takes longer than expected
- Insight 2: Refactoring is faster when you have clear examples to follow
- Insight 3: Documentation is often underestimated but critical for future reference

## Quality Metrics

### Code Quality
- **Test coverage**: ~85% (measured with `pytest --cov`)
- **Linting/Type checking**: Passed (Black formatting, Ruff linting)
- **Code review feedback**: Positive feedback on layering, type safety, and test coverage
- **Self-assessment**: 4/5 - Good structure, tests, and documentation; could improve with more edge case coverage

### Documentation Quality
- **Completeness**: Yes - README, API docs, learning notes, writeup all present
- **Clarity**: 4/5 - Clear explanations, but some sections could use more examples
- **Reusability**: Yes - Learning notes in `learning_notes/week2/` are well-organized for reference

### Learning Depth
- **Concept understanding**: 4/5 - Strong grasp of LLM integration, testing, and refactoring
- **Ability to explain to others**: 4/5 - Confident explaining Mock, Pydantic, structured output
- **Connection to previous weeks**: Builds on Week 1's prompt engineering foundation

## Next Steps

### Immediate (This Week)
- [ ] Add more edge case tests for LLM extraction (empty input, very long input, unicode)
- [ ] Experiment with larger models (llama3.1:70b) to compare extraction quality
- [ ] Add logging configuration to track LLM response times and success rates

### Short-term (Next Week)
- [ ] Learn advanced Pydantic features (validators, root_model, custom types)
- [ ] Explore caching LLM responses for repeated inputs
- [ ] Investigate prompt tuning for better action item recognition

### Long-term (Course Goals)
- [ ] Build a reusable LLM integration library based on Week 2 patterns
- [ ] Experiment with fine-tuning small models for specific extraction tasks
- [ ] Learn deployment strategies for LLM-powered applications (Docker, cloud)

## Questions for Future

### Unresolved Questions
- Question 1: How to handle LLM rate limits in production? (Currently using local Ollama, but cloud APIs have limits)
- Question 2: What's the best way to version prompts and schemas as the system evolves?
- Question 3: How to monitor LLM quality degradation over time? (Models can change, prompts can become stale)

### Topics to Revisit
- Topic 1: Advanced Pydantic patterns (computed fields, validation chains)
- Topic 2: LLM observability and monitoring (tracking token usage, latency, costs)
- Topic 3: Prompt engineering best practices (few-shot examples, chain-of-thought)

## Connection to Course Themes

### Stanford AI Engineering Mindset

**Build Systems, Not Just Code**:
- Week 2 demonstrates this through layered architecture: Router, Service, Database layers each have clear responsibilities
- System-level thinking: Testing strategy considers speed (Mock) vs confidence (real LLM), not just "write tests"
- Graceful degradation: System continues working even when LLM fails (returns empty list, doesn't crash)

### The Automation Hierarchy

**Current level achieved**: Level 2 (Reusable Functions)
- Evidence:
  - `extract_action_items_llm()` is a reusable LLM integration function
  - Mock test pattern is documented and reusable across tests
  - Pydantic schema pattern is repeatable for new endpoints
  - Factory methods eliminate repetitive construction code
- Next level goal: Level 3 (Composable System)
  - Create Warp saved prompts for LLM integration
  - Build automated test generation from schemas
  - Design system where new extraction tasks can be added with minimal code

### The Three Questions

1. **What's the bottleneck?**: Manual testing of LLM features (2-3s per test) and manual validation of API responses
2. **What's the leverage point?**: Mock tests for 60x speedup, Pydantic schemas for automatic validation, structured output to eliminate parsing errors
3. **How to compound value?**: Documented patterns (testing, refactoring, LLM integration) can be reused across all future LLM projects

## Quick Links

- [Overview](./overview.md) - Concepts and objectives
- [Implementation](./implementation.md) - Technical approach and decisions
- [Weekly Deliverable](../../week2/week2_writeup.md) - Submission writeup

---
*[Template: weekly_reflection.md - Last updated: 2026-01-02]*
